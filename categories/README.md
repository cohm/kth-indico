# Category tree for a KTH-wide Indico

A proposal for how KTH's events are organised in Indico: central management, the Faculty
Council, education networks, the five schools with their faculty boards and line organisation,
the University Administration, research centres and a sandbox. The line organisation carries
KTH's organisation codes (`S` → `SH` → `SHR`), so each category can later be linked to the
matching UG/LDAP group.

| File | What |
| --- | --- |
| [`kth-category-tree.md`](kth-category-tree.md) | the tree, its sources and the open questions. **Edit this one.** |
| [`tree.py`](tree.py) | checks the tree (duplicate codes, sibling titles, indentation) and exports it for the slide |
| [`make-categories.py`](make-categories.py) | creates the tree in Indico (`indico shell`, dry run unless `--commit`) |
| [`fetch-directory.py`](fetch-directory.py) | reads the line organisation and codes from KTH's public staff directory (units only, no people) |

## Workflow

After editing the tree, check it and refresh the slide data (Python 3, no packages needed):

```sh
python3 categories/tree.py --js slides/indico-kth-sv/category-tree.js
```

It prints warnings, errors and counts, and writes the file only if there are no errors.
Commit the `.md` and the `.js` together.

To compare the line organisation with KTH's directory (the directory changes when units are
reorganised):

```sh
python3 categories/fetch-directory.py S > /tmp/sci.md
```

then compare with the school's part of the tree by hand. The tree also holds categories that
are not units, so it is never regenerated wholesale.

## Creating the categories

On the server, as the `indico` user, with the three files copied to `/opt/indico/tmp/`:

```
indico shell -r
%run /opt/indico/tmp/make-categories.py PARENT_ID --verbose
%run /opt/indico/tmp/make-categories.py PARENT_ID --commit --map /opt/indico/tmp/codes.tsv
```

`PARENT_ID` is the category the tree goes under. Read the dry run before `--commit`. The script
creates missing categories and reuses existing ones (same title under the same parent). It never
renames, moves or deletes. Top-level categories are created protected. The code → category id
map stays on the server: category IDs are deployment details and are not committed here.
