"""Create local Indico accounts from a CSV and put them in a local group.

Run INSIDE `indico shell -r`, as the indico user (same pattern as gruppwebb/gw-import.py):

    %run /opt/indico/tmp/make-accounts.py CSV "GROUP NAME"            # dry run
    %run /opt/indico/tmp/make-accounts.py CSV "GROUP NAME" --commit

CSV    UTF-8, one person per line: first_name,last_name,email  (a header line starting with
       "first" is skipped). Personal data: copy it to /opt/indico/tmp/ for the run, delete it
       afterwards, never commit it.
GROUP  local group to create (or reuse) and add everyone to, e.g. "<your group name>".

Per person:
- email already belongs to an active user -> no new account, that user is added to the group;
- otherwise a new user (affiliation AFFILIATION below) with a local identity: username = the email's local
  part (made unique with a digit if taken), password = 32 random bytes that are never shown or
  stored anywhere else. The person sets their own password via "forgot password".
- Creating an account sends no mail (same code path as `indico user create`).

Mirrors `indico user create` in indico/cli/user.py and `create_user` in
indico/modules/users/operations.py (v3.3.14, read 2026-11-16).
Output is counts only unless --verbose.
"""
import argparse
import csv
import secrets
from uuid import uuid4

from indico.core.config import config
from indico.core.db import db
from indico.modules.auth import Identity
from indico.modules.groups.models.groups import LocalGroup
from indico.modules.users import User
from indico.modules.users.operations import create_user
from indico.util.string import validate_email

AFFILIATION = 'KTH Royal Institute of Technology'


def read_people(path):
    people = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        for row in csv.reader(f):
            if not row or not ''.join(row).strip():
                continue
            if row[0].strip().lower().startswith('first'):
                continue
            if len(row) != 3:
                raise SystemExit(f'Line {len(people) + 1}: expected 3 columns, got {len(row)}')
            first, last, email = (c.strip() for c in row)
            email = email.lower()
            if not validate_email(email, check_dns=False):
                raise SystemExit(f'Line {len(people) + 1}: not a valid email address')
            people.append((first, last, email))
    emails = [p[2] for p in people]
    if len(set(emails)) != len(emails):
        raise SystemExit('Duplicate email addresses in the CSV')
    return people


def free_username(email, taken):
    base = email.split('@')[0].lower()
    name, n = base, 1
    while name in taken or Identity.query.filter_by(provider='indico', identifier=name).has_rows():
        n += 1
        name = f'{base}{n}'
    taken.add(name)
    return name


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('csv')
    ap.add_argument('group')
    ap.add_argument('--commit', action='store_true', help='write to the database (default: dry run)')
    ap.add_argument('--verbose', action='store_true', help='print one line per person')
    args = ap.parse_args(argv)

    people = read_people(args.csv)
    group = LocalGroup.query.filter(db.func.lower(LocalGroup.name) == args.group.lower()).first()
    group_new = group is None
    if group_new:
        group = LocalGroup(name=args.group)
        db.session.add(group)

    created = existing = already_member = 0
    taken = set()
    for first, last, email in people:
        user = User.query.filter(User.all_emails == email, ~User.is_deleted, ~User.is_pending).first()
        if user:
            existing += 1
            what = 'exists'
        else:
            username = free_username(email, taken) if config.LOCAL_USERNAMES else str(uuid4())
            identity = Identity(provider='indico', identifier=username,
                                password=secrets.token_urlsafe(32))
            user = create_user(email, {'first_name': first, 'last_name': last,
                                       'affiliation': AFFILIATION}, identity)
            created += 1
            what = f'new, username {username}'
        if user in group.members:
            already_member += 1
        group.members.add(user)
        if args.verbose:
            print(f'  {email}: {what}')

    db.session.flush()
    print(f'Group "{group.name}": {"NEW" if group_new else "existing"}, id {group.id}, '
          f'{len(group.members)} members after this run')
    print(f'People in CSV: {len(people)} | new accounts: {created} | existing accounts: {existing} '
          f'| already in group: {already_member}')
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
