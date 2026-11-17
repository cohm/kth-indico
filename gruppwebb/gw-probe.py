#!/usr/bin/env python3
"""Answer the questions the importer depends on, with counts only: no titles, names or text.

Follows gw-schema.py. The schema showed one merged list of items: events (with `details`), file
records (with `file_id`), members (with `email`) and other content (pages, posts, links). This
probe reports, per JSON file and in total:
- how many items of each kind there are, and the values of a few enumeration fields (`type`,
  `context_type`, activity `type`, MIME types). These are printed only if they look like
  enumeration values: short lowercase identifiers or MIME types, and at most 25 distinct;
- for events: start hour, weekday, duration and cancellation counts (to settle the timezone and
  whether end times are real), and how many titles are distinct;
- for files: whether `local_path` exists on disk, and how a file is tied to an event. For each
  candidate link (an event's `_id`, `slug` or `context_id` inside the file's `original_url` or
  `local_path`, or a file's id or name inside an event's `body` or activity), it counts the matches.

READ THE OUTPUT BEFORE SHARING IT, as with gw-schema.py.

Usage:  python3 -I gw-probe.py EXPORT_DIR > probe.txt
"""
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

ENUM = re.compile(r'^[a-z][a-z0-9_\-]{0,24}$')
MIME = re.compile(r'^[a-z]+/[a-z0-9.+\-]{1,80}$')
STRUCT_NAME = re.compile(r'^[a-z_][a-z0-9_\-]{0,20}\.json$')


def enum_report(label, counter, out):
    vals = [v for v in counter if isinstance(v, str)]
    if not vals:
        out.append(f'  {label}: (no string values)')
    elif len(vals) <= 25 and all(ENUM.match(v) or MIME.match(v) for v in vals):
        out.append(f'  {label}: ' + ', '.join(f'{v}×{n}' for v, n in counter.most_common()))
    else:
        out.append(f'  {label}: {len(vals)} distinct values, not shown (not enumeration-like)')


def kind(item):
    if not isinstance(item, dict):
        return type(item).__name__
    if 'details' in item:
        return 'event-like (has details)'
    if 'file_id' in item:
        return 'file record'
    if 'email' in item:
        return 'member'
    if 'body' in item:
        return 'other content (body, no details)'
    return 'other'


def parse(ts):
    try:
        return datetime.fromisoformat(ts)
    except (TypeError, ValueError):
        return None


def main():
    root = os.path.abspath(sys.argv[1])
    if not os.path.isdir(root):
        sys.exit(f'Not a directory: {root}')
    jfiles = sorted(os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.lower().endswith('.json'))
    if not jfiles:
        sys.exit(f'No .json files under {root}')
    out = ['# Gruppwebben export probe (counts only). Review before sharing.', '']

    items = []          # (file label, item)
    out.append('## JSON files')
    for i, path in enumerate(jfiles):
        base = os.path.basename(path)
        label = base if STRUCT_NAME.match(base) else f'file#{i}.json'
        with open(path, encoding='utf-8-sig') as fh:
            data = json.load(fh)
        if isinstance(data, list):
            kinds = Counter(kind(x) for x in data)
            out.append(f'  {label}: array of {len(data)} — ' + ', '.join(f'{k}×{n}' for k, n in kinds.most_common()))
            items += [(label, x) for x in data]
        else:
            out.append(f'  {label}: object with keys ' + ', '.join(sorted(data)))
    out.append('')

    # all_content.json repeats events.json etc.: count each item once (by _id, else file_id)
    seen, dicts = set(), []
    for _, x in items:
        if not isinstance(x, dict):
            continue
        key = x.get('_id') or x.get('file_id') or id(x)
        if key not in seen:
            seen.add(key)
            dicts.append(x)
    out.append(f'  unique items after removing repeats: {len(dicts)} (of {len(items)})')
    out.append('')
    events = [x for x in dicts if 'details' in x]
    files = [x for x in dicts if 'file_id' in x]
    content = [x for x in dicts if 'body' in x]

    out.append('## Enumeration fields')
    enum_report('item type', Counter(x.get('type') for x in content), out)
    enum_report('event type', Counter(x.get('type') for x in events), out)
    enum_report('context_type', Counter(x.get('context_type') for x in content), out)
    enum_report('activity type', Counter(a.get('type') for x in content for a in x.get('activity') or []), out)
    enum_report('tracking operation', Counter(t.get('operation') for x in content for t in x.get('tracking_comments') or []), out)
    enum_report('file content_type', Counter(x.get('content_type') for x in files), out)
    out.append('')

    out.append(f'## Events ({len(events)})')
    starts, durs, weekday, hour, cancelled, no_time = [], Counter(), Counter(), Counter(), 0, 0
    for e in events:
        d = e['details']
        s, t = parse(d.get('start_time')), parse(d.get('end_time'))
        if d.get('is_cancelled'):
            cancelled += 1
        if not s:
            no_time += 1
            continue
        hour[s.hour] += 1
        weekday[s.strftime('%a')] += 1
        if t:
            durs[int((t - s).total_seconds() // 60)] += 1
        starts.append(s)
    out.append(f'  cancelled: {cancelled}; without a parseable start: {no_time}')
    out.append('  start hour: ' + ', '.join(f'{h:02d}h×{n}' for h, n in sorted(hour.items())))
    out.append('  weekday: ' + ', '.join(f'{d}×{n}' for d, n in weekday.most_common()))
    out.append('  duration (min): ' + ', '.join(f'{m}×{n}' for m, n in sorted(durs.items())))
    tz = Counter('aware' if s.tzinfo else 'naive' for s in starts)
    out.append(f'  start_time timezone info: {dict(tz)}')
    titles = Counter(e.get('title') for e in events)
    out.append(f'  distinct titles: {len(titles)}; the most common title is used by {titles.most_common(1)[0][1] if titles else 0} events')
    bodies = [e.get('body') or '' for e in events]
    out.append(f'  body: empty×{sum(1 for b in bodies if not b.strip())}, '
               f'with <a href×{sum(1 for b in bodies if "<a " in b)}, '
               f'with <img×{sum(1 for b in bodies if "<img" in b)}, '
               f'with <table×{sum(1 for b in bodies if "<table" in b)}')
    out.append('')

    out.append(f'## Files ({len(files)})')
    exist = sum(1 for f in files if f.get('local_path') and os.path.isfile(os.path.join(root, f['local_path'])))
    out.append(f'  local_path exists on disk: {exist}/{len(files)}')
    ev_keys = {}
    for e in events:
        for field in ('_id', 'slug', 'context_id'):
            v = e.get(field)
            if v not in (None, ''):
                ev_keys.setdefault(field, {})[str(v)] = e
    for field, table in ev_keys.items():
        for ffield in ('original_url', 'local_path'):
            hits = sum(1 for f in files if any(k in (f.get(ffield) or '') for k in table if len(k) >= 6))
            out.append(f'  event {field} found in file {ffield}: {hits}/{len(files)}')
    texts = [(e.get('body') or '') + ' '.join((a.get('data') or {}).get('new_content') or ''
                                              for a in e.get('activity') or []) for e in events]
    alltext = '\n'.join(texts)
    for ffield in ('file_id', 'saved_as', 'original_name', 'original_url'):
        vals = [f.get(ffield) for f in files if f.get(ffield)]
        in_any = sum(1 for v in vals if v in alltext)
        out.append(f'  file {ffield} found in event body/activity text: {in_any}/{len(vals)}')
    per_event = Counter()
    for f in files:
        fid = f.get('file_id') or ''
        n = sum(1 for t in texts if fid and fid in t)
        per_event[n] += 1
    out.append('  files by number of events that mention their file_id: '
               + ', '.join(f'{k} events×{n}' for k, n in sorted(per_event.items())))
    # URL shape: a segment is shown only if it is a short lowercase word in at least half of the
    # URLs at that position (structural, like "files"); anything else becomes x.
    segs = [(f.get('original_url') or '').split('/') for f in files]
    common = Counter((i, s) for p in segs for i, s in enumerate(p) if re.fullmatch(r'[a-z]{2,12}', s))
    keep = {k for k, n in common.items() if n >= len(files) / 2}
    shapes = Counter('/'.join(s if (i, s) in keep else ('' if s == '' else 'x') for i, s in enumerate(p))
                     for p in segs)
    out.append('  original_url shape: ' + ', '.join(f'{s}×{n}' for s, n in shapes.most_common(5)))

    # Activity entries that point at another object (24 in the schema: subject_name/_type_slug/_url)
    subj = [(e, a['data']) for e in events for a in e.get('activity') or []
            if isinstance(a.get('data'), dict) and a['data'].get('subject_url')]
    out.append(f'  event activity entries with a subject_url: {len(subj)} '
               f'(in {len({id(e) for e, _ in subj})} events)')
    enum_report('  their activity type', Counter(a.get('type') for e in events for a in e.get('activity') or []
                                                if isinstance(a.get('data'), dict) and a['data'].get('subject_url')), out)
    enum_report('  their subject_type_slug', Counter(d.get('subject_type_slug') for _, d in subj), out)
    fids = [f.get('file_id') for f in files if f.get('file_id')]
    hit = sum(1 for _, d in subj if any(fid in d['subject_url'] for fid in fids))
    out.append(f'  subject_urls containing a file_id: {hit}/{len(subj)}')
    hit = sum(1 for _, d in subj if any(d['subject_url'] in (f.get('original_url') or '') or
                                        (f.get('original_url') or '') in d['subject_url'] for f in files))
    out.append(f'  subject_urls equal to/contained in a file original_url: {hit}/{len(subj)}')

    # Dates in file names vs. meeting dates
    ev_dates = Counter(s.date() for s in starts)
    rxs = [(r'(20\d\d)-(\d\d)-(\d\d)', 'ymd'), (r'(20\d\d)(\d\d)(\d\d)', 'ymd'), (r'(?<!\d)(\d\d)(\d\d)(\d\d)(?!\d)', 'yymmdd'),
           (r'(\d\d)[./-](\d\d)[./-](20\d\d)', 'dmy')]
    matched, with_date = 0, 0
    for f in files:
        name = f.get('original_name') or ''
        found = None
        for rx, kind_ in rxs:
            m = re.search(rx, name)
            if not m:
                continue
            a, b, c = (int(g) for g in m.groups())
            y, mo, d = {'ymd': (a, b, c), 'yymmdd': (2000 + a, b, c), 'dmy': (c, b, a)}[kind_]
            try:
                found = datetime(y, mo, d).date()
                break
            except ValueError:
                continue
        if found:
            with_date += 1
            if found in ev_dates:
                matched += 1
    out.append(f'  file names with a date: {with_date}/{len(files)}; of those on a meeting day: {matched}')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
