"""Import a KTH Gruppwebben meeting series into an Indico category.

Run INSIDE `indico shell -r` (a request context is needed for session.user), as the indico user:

    %run /opt/indico/tmp/gw-import.py EXPORT_DIR CATEGORY_ID USER_ID            # dry run
    %run /opt/indico/tmp/gw-import.py EXPORT_DIR CATEGORY_ID USER_ID --commit

EXPORT_DIR   the unpacked export (events.json, files_manifest.json, files/)
CATEGORY_ID  target category, from its URL /category/<id>/. Make it PROTECTED first.
USER_ID      the Indico user recorded as creator and uploader (an admin, e.g. your own).

Mapping (from gw-schema.py / gw-probe.py, 2026-11-01; written without reading the data):
- every item in events.json with type "event" → one Indico *meeting*
  title ← title, start/end ← details.start_time/end_time (naive, Europe/Stockholm, summer time
  included), room ← details.location[0];
- each meeting gets ONE contribution, "Info and discussions", spanning the whole meeting.
  Its description ← body (HTML render mode), and the files are its material. The event's own
  description stays empty;
- cancelled meetings (details.is_cancelled): --cancelled mark (default) puts "[Cancelled] " in
  front of the title, --cancelled skip leaves them out;
- a file in files_manifest.json is attached (to that contribution) in every meeting whose body or edit history
  contains its file_id (56/57 in the probe; 5 files belong to two meetings);
- images are NOT rendered: each <img> in the body becomes a link, named after the file, to its
  attachment (pasted data:-URI images become attachments of their own; external images become
  a plain link); other links to an attached file are rewritten to the Indico copy;
- attachments keep their original file names;
- not imported: members, watchers, comments, edit history, tracking, pages/descriptions.

Re-running is safe: a meeting with the same title and start time already in the category is skipped.
Output is counts only, so it can be shared.
"""
import argparse
import base64
import html
import io
import json
import mimetypes
import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import g, session

from indico.core.db import db
from indico.core.db.sqlalchemy.descriptions import RenderMode
from indico.modules.attachments.models.attachments import Attachment, AttachmentFile, AttachmentType
from indico.modules.attachments.models.folders import AttachmentFolder
from indico.modules.categories.models.categories import Category
from indico.modules.events.contributions.models.contributions import Contribution
from indico.modules.events.contributions.operations import create_contribution
from indico.modules.events.models.events import Event, EventType
from indico.modules.events.operations import create_event
from indico.modules.users import User
from indico.util.fs import secure_client_filename

LOCAL_TZ = ZoneInfo('Europe/Stockholm')
CONTRIB_TITLE = 'Info and discussions'


def to_utc(naive_iso):
    local = datetime.fromisoformat(naive_iso).replace(tzinfo=LOCAL_TZ)
    return local.astimezone(timezone.utc)


IMG = re.compile(r'<img\b[^>]*>', re.I)
DATA_URI = re.compile(r'^data:(image/[\w.+\-]+);base64,(.*)$', re.S)


def img_attr(tag, name):
    m = re.search(r'\b' + name + r'\s*=\s*("([^"]*)"|\'([^\']*)\')', tag, re.I)
    return (m.group(2) if m.group(2) is not None else m.group(3)) if m else ''


def img_kind(src, files_by_id):
    if any(fid in src for fid in files_by_id):
        return 'file'
    if DATA_URI.match(src):
        return 'data-uri'
    return 'other'


def history_text(item):
    parts = [item.get('body') or '']
    for a in item.get('activity') or []:
        d = a.get('data') or {}
        parts += [d.get('new_content') or '', d.get('content') or '']
    return '\n'.join(parts)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('export_dir')
    ap.add_argument('category_id', type=int)
    ap.add_argument('user_id', type=int)
    ap.add_argument('--cancelled', choices=['mark', 'skip'], default='mark')
    ap.add_argument('--commit', action='store_true', help='write to the database (default: dry run)')
    args = ap.parse_args(argv)

    root = os.path.abspath(args.export_dir)
    with open(os.path.join(root, 'events.json'), encoding='utf-8-sig') as fh:
        items = [x for x in json.load(fh) if x.get('type') == 'event']
    with open(os.path.join(root, 'files_manifest.json'), encoding='utf-8-sig') as fh:
        files = json.load(fh)

    category = Category.get(args.category_id)
    user = User.get(args.user_id)
    if category is None or user is None:
        raise SystemExit(f'category {args.category_id} or user {args.user_id} not found')
    session.set_session_user(user)
    stats = Counter()
    if not category.is_protected:
        print(f'WARNING: category {category.id} is NOT protected: the imported meetings would be '
              f'public. Protect it first (category → Settings → Protection).')
        if args.commit:
            raise SystemExit('Refusing to import into an unprotected category.')

    existing = {(e.title, e.start_dt) for e in Event.query.filter_by(category=category, is_deleted=False)}
    files_by_id = {f['file_id']: f for f in files if f.get('file_id')}
    used_files = set()

    for item in sorted(items, key=lambda x: (x.get('details') or {}).get('start_time') or ''):
        d = item.get('details') or {}
        if not d.get('start_time'):
            stats['skipped: no start time'] += 1
            continue
        title = item.get('title') or 'Meeting'
        if d.get('is_cancelled'):
            if args.cancelled == 'skip':
                stats['skipped: cancelled'] += 1
                continue
            title = '[Cancelled] ' + title
            stats['cancelled, marked'] += 1
        start = to_utc(d['start_time'])
        end = to_utc(d['end_time']) if d.get('end_time') else None
        if not end or end <= start:
            end = start + timedelta(hours=1)
            stats['end missing/invalid → 1 h'] += 1
        if (title, start) in existing:
            stats['skipped: already imported'] += 1
            continue

        text = history_text(item)
        my_files = [f for fid, f in files_by_id.items() if fid in text]
        used_files.update(f['file_id'] for f in my_files)
        stats['meetings'] += 1
        stats['attachments'] += len(my_files)
        stats['attachment files missing on disk'] += sum(
            1 for f in my_files if not os.path.isfile(os.path.join(root, f.get('local_path') or '')))
        for tag in IMG.findall(item.get('body') or ''):
            stats[f'images → link ({img_kind(img_attr(tag, "src"), files_by_id)})'] += 1
        if not args.commit:
            continue

        loc = ((d.get('location') or [''])[0] or '').strip()
        location_data = ({'inheriting': False, 'room_name': loc, 'venue_name': '', 'address': ''}
                         if loc else {'inheriting': True})
        event = create_event(category, EventType.meeting, {
            'title': title,
            'start_dt': start,
            'end_dt': end,
            'timezone': 'Europe/Stockholm',
            'location_data': location_data,
        }, add_creator_as_manager=False)
        # A contribution's friendly id normally comes from increment_and_get(), which bumps
        # Event._last_friendly_contribution_id in a SEPARATE transaction. That transaction can't see
        # this still-uncommitted event, so it returns no row (TypeError in v3.3.14). Pre-allocate
        # id 1 instead, the way _get_next_friendly_id() allows, so that the whole import stays one
        # transaction.
        g.setdefault('friendly_ids', {}).setdefault(Contribution, {})[event.id] = [1]
        event._last_friendly_contribution_id = 1
        # One timetable entry spanning the meeting; it carries the notes and the material.
        contrib = create_contribution(event, {
            'title': CONTRIB_TITLE,
            'start_dt': start,
            'duration': end - start,
            'render_mode': RenderMode.html,
        })

        body = item.get('body') or ''
        folder = None

        def attach(name, ctype, fileobj):
            nonlocal folder
            if folder is None:
                folder = AttachmentFolder.get_or_create_default(linked_object=contrib)
            if not ctype or ctype == 'application/octet-stream':
                ctype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
            # title and download name keep the original file name (secure_client_filename only
            # strips path separators and control characters)
            att = Attachment(folder=folder, user=user, title=name, type=AttachmentType.file)
            att.file = AttachmentFile(user=user, filename=secure_client_filename(name), content_type=ctype)
            att.file.save(fileobj)
            db.session.add(att)
            db.session.flush()
            return att

        atts = {}
        for f in my_files:
            path = os.path.join(root, f['local_path'])
            name = f.get('original_name') or f.get('saved_as') or os.path.basename(path)
            with open(path, 'rb') as fh:
                atts[f['file_id']] = attach(name, f.get('content_type'), fh)

        # Images are NOT rendered: each <img> becomes a link, named after the file, to its attachment.
        n_inline = 0

        def img_to_link(m):
            nonlocal n_inline
            tag = m.group(0)
            src = img_attr(tag, 'src')
            for fid, att in atts.items():
                if fid in src:
                    return f'<a href="{att.download_url}">{html.escape(att.title)}</a>'
            if dm := DATA_URI.match(src):
                # pasted image without a file: becomes an attachment of its own
                n_inline += 1
                ext = mimetypes.guess_extension(dm.group(1)) or '.img'
                name = (img_attr(tag, 'data-filename') or img_attr(tag, 'title')
                        or f'image-{n_inline}{ext}')
                att = attach(name, dm.group(1), io.BytesIO(base64.b64decode(dm.group(2))))
                return f'<a href="{att.download_url}">{html.escape(att.title)}</a>'
            name = os.path.basename(src.split('?')[0]) or 'image'
            return f'<a href="{html.escape(src)}">{html.escape(name)}</a>'

        body = IMG.sub(img_to_link, body)
        # Remaining links to an attached file point at the Indico copy.
        for fid, att in atts.items():
            pat = re.compile(r'((?:href|src)=")[^"]*' + re.escape(fid) + r'[^"]*(")')
            body, n = pat.subn(lambda m: m.group(1) + att.download_url + m.group(2), body)
            stats['links rewritten'] += n
        contrib.description = body
        db.session.flush()

    stats['files never attached'] = len(set(files_by_id) - used_files)
    if args.commit:
        db.session.commit()
        print('COMMITTED.')
    else:
        print('DRY RUN: nothing written. Add --commit to import.')
    for k, v in sorted(stats.items()):
        print(f'  {k}: {v}')


try:
    main()
except BaseException:
    # leave the shell's session usable for a re-run (nothing has been committed)
    db.session.rollback()
    raise
