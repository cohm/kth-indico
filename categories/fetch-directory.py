#!/usr/bin/env python3
"""Print KTH's line organisation (school -> department -> division) as tree lines for
kth-category-tree.md, read from the public staff directory at https://www.kth.se/directory.

Only unit links are read (codes and names). The people listed on the same pages are skipped:
nothing about them is parsed, printed or stored.

    python3 fetch-directory.py            # all schools and the University Administration
    python3 fetch-directory.py S T        # only these top-level codes

Output: one line per unit in the format kth-category-tree.md uses, two spaces per level:

    - `SH` Physics · *Fysik*

The directory has three levels (school/department/division) for most schools. Use the output
to refresh or diff the tree by hand; the tree file also holds categories that are not units
(committees, networks, centres), so it is not regenerated wholesale.
"""
import html
import os
import re
import subprocess
import sys
import tempfile
import time

BASE = 'https://www.kth.se'
UNIT_LINK = re.compile(r'<a [^>]*href="(/directory/[a-z0-9/]+)"[^>]*>(.*?)</a>', re.S)
# The directory keeps the language in a cookie, so each language gets its own cookie jar.
# curl rather than urllib: urllib loops on the language redirect and is cut off by some proxies.
JARS = tempfile.mkdtemp(prefix='kth-directory-')


def units(path, lang):
    """Direct sub-units of a directory path, as {path: name}."""
    jar = os.path.join(JARS, lang)
    page = subprocess.run(['curl', '-sSfL', '--max-time', '30', '-A', 'kth-indico fetch-directory',
                           '-c', jar, '-b', jar, f'{BASE}{path}?l={lang}'],
                          capture_output=True, check=True).stdout.decode('utf-8', 'replace')
    depth = path.rstrip('/').count('/') + 1
    found = {}
    for href, text in UNIT_LINK.findall(page):
        href = href.rstrip('/')
        if href.startswith(path.rstrip('/') + '/') and href.count('/') == depth:
            found[href] = html.unescape(re.sub(r'<[^>]+>|\s+', ' ', text)).strip()
    return found


def walk(path, level, max_level=3):
    en, sv = units(path, 'en'), units(path, 'sv')
    for href in sorted(en, key=lambda h: en[h].lower()):
        code = href.rsplit('/', 1)[1].upper()
        alt = f' · *{sv[href]}*' if sv.get(href) and sv[href] != en[href] else ''
        print(f"{'  ' * (level - 1)}- `{code}` {en[href]}{alt}")
        if level < max_level:
            time.sleep(0.2)  # be gentle with kth.se
            walk(href, level + 1, max_level)


if __name__ == '__main__':
    wanted = {c.upper() for c in sys.argv[1:]}
    top_en, top_sv = units('/directory', 'en'), units('/directory', 'sv')
    for href in sorted(top_en):
        code = href.rsplit('/', 1)[1].upper()
        if not wanted or code in wanted:
            sv = top_sv.get(href, '')
            print(f"- `{code}` {top_en[href]}" + (f' · *{sv}*' if sv and sv != top_en[href] else ''))
            walk(href, 2)
