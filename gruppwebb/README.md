# Import from KTH Gruppwebben into Indico

Gruppwebben closes in autumn 2026. Sources:
- [Gruppwebben och Social stänger hösten 2026](https://intra.kth.se/utbildning/e-larande/e-larande-nyheter/gruppwebben-och-social-stanger-hosten-2026-1.1493255)
- [Gruppwebben som samarbetsyta stängs hösten 2026](https://intra.kth.se/utbildning/nyheter/gruppwebben-som-samarbetsyta-stangs-hosten-2026-1.1462814)

Goal: turn a group's exported meeting series (JSON + attached files) into events in an Indico
category, both as demo content and as a migration path for others.

**Ground rule: the export contains personal data, and it is never read by the assistant that writes
these scripts.** Work goes by structure only.

## 1. Look at the structure (on your own computer)

**`gw-schema.py`** prints the layout, file types and merged JSON schema, with every value reduced to
a class (`datetime`, `email`, `html`, `text` with a length range, …). Path components and JSON keys
that look like data become `<name>`, `<int-string>`, `<key:…>` and so on. It's a heuristic: **read
the report before sharing it**. A mapping keyed by plain short names, such as `{"erik": …}`, could
still show keys.
```
python3 -I gw-schema.py ~/path/to/export > schema.txt
```
**`gw-probe.py`** follows up with counts only: item kinds per JSON file, enumeration values, event
start hours, weekdays and durations (to settle the timezone), and how files are tied to events.
```
python3 -I gw-probe.py ~/path/to/export > probe.txt
```

What the exports seen so far look like:
- one merged item list; the meetings are items with `details` (`start_time`/`end_time` naive,
  location, `is_cancelled`) and an HTML `body`. `events.json` holds the meetings;
  `all_content.json` repeats them plus pages and descriptions;
- file records (`file_id`, `original_name`, `local_path` → `files/…`, `original_url`,
  `content_type`), a member list, and a few pages, posts and links;
- per item, the edit history (`activity[].data.old_content/new_content/diff`), comments, watchers
  and tracking. These are not imported.
- Times are **naive Stockholm local time** (start hours and weekdays cluster on the group's
  meeting slot).
- Files belong to meetings by **`file_id` appearing in the body or edit history**. Other candidates
  (IDs in `original_url`, `subject_url` entries, which turned out to be comments, and dates in file
  names) don't link them.

## 2. Import (on the Indico server)

**`gw-import.py`** runs via `%run` inside `indico shell -r` and is a dry run unless `--commit` is
given. Its docstring gives the full mapping.
- It refuses to commit into an unprotected category, and skips meetings already imported with the
  same title and start time, so re-running is safe.
- Each meeting gets one contribution, "Info and discussions", spanning the meeting. It holds the
  notes (the Gruppwebben body, in HTML render mode) and the files as its material, so the meeting
  page shows them in the timetable.
- Images in the notes are not rendered: each becomes a link, named after the file, to its
  attachment. Body links and images that point at an attached file are rewritten to the Indico
  copy. Attachments keep their original file names.
- Indico API used, checked against the v3.3.14 source: `create_event`,
  `Attachment`/`AttachmentFile.save`, `AttachmentFolder.get_or_create_default`,
  `session.set_session_user`. The internal Python API is used because, as far as known, the HTTP
  API is for export only (not re-checked).

Copy the export to a temporary directory on the server for the run and delete it afterwards. The
imported files then live in Indico's archive.

Before committing, check the target in `indico shell`: `Category.get(N)` → title, parent,
`protection_mode`, no children. Category IDs follow creation order, not the tree.

**Privacy in Indico:** import into a **protected** category, with access for the group members only.
Meeting descriptions, minutes and attachments carry colleagues' names. They must not land in a
public category.
