"""Create the category tree in kth-category-tree.md under an existing Indico category.

Run INSIDE `indico shell -r`, as the indico user (same pattern as accounts/make-accounts.py).
Copy tree.py, make-categories.py and kth-category-tree.md to /opt/indico/tmp/ first.

    %run /opt/indico/tmp/make-categories.py PARENT_ID                  # dry run
    %run /opt/indico/tmp/make-categories.py PARENT_ID --commit
    %run /opt/indico/tmp/make-categories.py PARENT_ID --map codes.tsv  # also write code -> id

PARENT_ID  the category the tree goes under (0 is Indico's root). Not committed anywhere:
           category IDs are deployment details.

- Idempotent: a category whose parent already has a child with the same title is reused, not
  created again. Nothing is renamed, moved or deleted, so a renamed line in the tree file
  gives a new category next to the old one. Rename in Indico first, then in the file.
- New categories directly under PARENT_ID are created *protected*; everything below inherits.
- --map writes one line per organisation code: code, category id, path. Keep it with the
  deployment; it is what a later UG/LDAP sync needs.
- Refuses to run if tree.py finds errors (duplicate codes or sibling titles).

Uses create_category() in indico/modules/categories/operations.py and the Category model in
indico/modules/categories/models/categories.py (v3.3.14, read 2026-11-26).
"""
import argparse
import os
import sys
from contextlib import nullcontext

from flask import current_app, has_request_context

from indico.core.db import db
from indico.core.db.sqlalchemy.protection import ProtectionMode
from indico.modules.categories.models.categories import Category
from indico.modules.categories.operations import create_category

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tree import DEFAULT_TREE, check, parse, walk  # noqa: E402


def ensure(parent, node, top_level, stats, verbose, depth):
    existing = (Category.query
                .filter_by(parent_id=parent.id, title=node['title'], is_deleted=False)
                .first())
    if existing:
        stats['existing'] += 1
        category = existing
    else:
        data = {'title': node['title']}
        if top_level:
            data['protection_mode'] = ProtectionMode.protected
        category = create_category(parent, data)
        stats['new'] += 1
    if verbose:
        print(f"{'  ' * depth}{'=' if existing else '+'} {node['title']} (id {category.id})")
    for child in node['children']:
        ensure(category, child, False, stats, verbose, depth + 1)
    node['category'] = category


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('parent_id', type=int)
    ap.add_argument('--tree', default=str(DEFAULT_TREE), help='tree file (default: next to this script)')
    ap.add_argument('--commit', action='store_true', help='write to the database (default: dry run)')
    ap.add_argument('--map', metavar='FILE', help='write organisation code -> category id (TSV)')
    ap.add_argument('--verbose', action='store_true', help='one line per category: + new, = existing')
    args = ap.parse_args(argv)

    roots = parse(args.tree)
    errors, warnings = check(roots)
    if errors:
        raise SystemExit('Tree has errors, run tree.py on it:\n  ' + '\n  '.join(errors))
    parent = Category.get(args.parent_id, is_deleted=False)
    if parent is None:
        raise SystemExit(f'No category {args.parent_id}')

    stats = {'new': 0, 'existing': 0}
    # create_category() logs with session.user; give it a request context if the shell has none.
    ctx = nullcontext() if has_request_context() else current_app.test_request_context()
    with ctx:
        for node in roots:
            ensure(parent, node, True, stats, args.verbose, 0)
        db.session.flush()

    print(f'Under "{parent.title}": {stats["new"]} new, {stats["existing"]} existing '
          f'({len(warnings)} warnings from tree.py)')
    if args.map:
        with open(args.map, 'w', encoding='utf-8') as f:
            for node, _, _ in walk(roots):
                if node['code']:
                    cat = node['category']
                    f.write(f"{node['code']}\t{cat.id}\t{' » '.join(cat.chain_titles[1:])}\n")
        print(f'Wrote {args.map}' + ('' if args.commit else ' (dry run: the ids of new categories are not kept)'))
    if args.commit:
        db.session.commit()
        print('COMMITTED.')
    else:
        db.session.rollback()
        print('DRY RUN: nothing written. Add --commit to create.')


try:
    main()
except BaseException:
    # leave the shell's session usable for a re-run (nothing has been committed)
    db.session.rollback()
    raise
