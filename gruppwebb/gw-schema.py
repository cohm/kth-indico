#!/usr/bin/env python3
"""Describe the STRUCTURE of a KTH Gruppwebben export without revealing its content.

Prints a report that is meant to be read by someone who must not see the data: directory and file
layout, file types and sizes, and for JSON files the merged schema (keys, types, array lengths,
string formats). Values are never printed. They are reduced to classes such as `datetime`,
`email`, `html`, `text` (with a length range), and for dates only the year range.

Names are what can leak, so they are reduced too:
- A path component is printed literally only if it looks structural: a short plain identifier
  (e.g. `files`, `meeting.json`) that occurs at least --min-repeat times in the tree. Anything else
  becomes a class, such as <int>, <date>, <uuid> or <name>, with the file extension kept.
- JSON keys are printed only if every key in that object is a plain identifier, and the object
  doesn't look like a mapping keyed by data: too many distinct keys, most of them rare. Otherwise
  the keys become <key:CLASS>.

It's a heuristic. READ THE OUTPUT YOURSELF BEFORE SHARING IT.

Usage:  python3 -I gw-schema.py EXPORT_DIR > schema.txt
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

IDENT = re.compile(r'^[A-Za-z_][A-Za-z0-9_\-]{0,30}$')
STRUCT_NAME = re.compile(r'^[a-z_][a-z0-9_\-]{0,20}(\.[a-z0-9]{1,5})?$')
STRING_CLASSES = [
    ('uuid', re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')),
    ('datetime', re.compile(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}')),
    ('date', re.compile(r'^\d{4}-\d{2}-\d{2}$')),
    ('time', re.compile(r'^\d{1,2}:\d{2}(:\d{2})?$')),
    ('int-string', re.compile(r'^-?\d+$')),
    ('decimal-string', re.compile(r'^-?\d+[.,]\d+$')),
    ('hex-id', re.compile(r'^[0-9a-fA-F]{16,}$')),
    ('email', re.compile(r'^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$')),
    ('url', re.compile(r'^(https?|ftp|mailto):', re.I)),
    ('rel-path', re.compile(r'^[^\s<>]*[/\\][^\s<>]*\.[A-Za-z0-9]{1,5}$')),
]
HTML = re.compile(r'</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>')
YEAR = re.compile(r'^(\d{4})-\d{2}-\d{2}')


def classify(s):
    if s == '':
        return 'empty'
    for label, rx in STRING_CLASSES:
        if rx.match(s):
            return label
    if HTML.search(s):
        return 'html'
    return 'multiline-text' if '\n' in s else 'text'


def name_class(name):
    stem, ext = os.path.splitext(name)
    c = classify(stem)
    c = {'text': 'name', 'multiline-text': 'name', 'html': 'name', 'email': 'name'}.get(c, c)
    return f'<{c}>{ext.lower()}'


class Node:
    def __init__(self):
        self.n = 0
        self.types = Counter()
        self.keys = defaultdict(Node)
        self.items = None
        self.alen = []
        self.scls = Counter()
        self.slen = []
        self.years = []
        self.idigits = Counter()

    def observe(self, v):
        self.n += 1
        if isinstance(v, dict):
            self.types['object'] += 1
            for k, sub in v.items():
                self.keys[k].observe(sub)
        elif isinstance(v, list):
            self.types['array'] += 1
            self.alen.append(len(v))
            if self.items is None:
                self.items = Node()
            for sub in v:
                self.items.observe(sub)
        elif isinstance(v, bool):
            self.types['bool'] += 1
        elif isinstance(v, int):
            self.types['int'] += 1
            self.idigits[len(str(abs(v)))] += 1
        elif isinstance(v, float):
            self.types['float'] += 1
        elif v is None:
            self.types['null'] += 1
        else:
            self.types['string'] += 1
            c = classify(v)
            self.scls[c] += 1
            self.slen.append(len(v))
            m = YEAR.match(v)
            if m:
                self.years.append(int(m.group(1)))

    def keys_are_data(self):
        ks = list(self.keys)
        if not all(IDENT.match(k) for k in ks):
            return True
        n_obj = self.types['object'] or 1
        rare = sum(1 for k in ks if self.keys[k].n < 0.1 * n_obj)
        return len(ks) > 30 and rare > len(ks) / 2

    def render(self, indent, out):
        pad = '  ' * indent
        parts = [f'{t}×{c}' for t, c in self.types.most_common()]
        line = ', '.join(parts)
        if self.scls:
            line += ' | str: ' + ', '.join(f'{c}×{n}' for c, n in self.scls.most_common())
            line += f' | len {min(self.slen)}–{max(self.slen)}'
        if self.years:
            line += f' | years {min(self.years)}–{max(self.years)}'
        if self.idigits:
            line += ' | int digits ' + ','.join(str(d) for d in sorted(self.idigits))
        if self.alen:
            line += f' | array len {min(self.alen)}–{max(self.alen)}'
        out.append(line)
        if self.keys:
            if self.keys_are_data():
                merged = defaultdict(Node)
                kcls = Counter()
                for k, sub in self.keys.items():
                    label = f'<key:{name_class(k)[1:].split(">")[0]}>'
                    kcls[label] += 1
                    _merge(merged[label], sub)
                for label, sub in sorted(merged.items()):
                    out.append(f'{pad}  {label} ({kcls[label]} distinct, seen {sub.n}×): ')
                    sub.render(indent + 2, out)
            else:
                n_obj = self.types['object'] or 1
                for k, sub in sorted(self.keys.items()):
                    out.append(f'{pad}  {k} [{sub.n}/{n_obj}]: ')
                    sub.render(indent + 2, out)
        if self.items is not None and self.items.n:
            out.append(f'{pad}  [items]: ')
            self.items.render(indent + 2, out)


def _merge(dst, src):
    """Fold src's observations into dst (used when collapsing data-like keys)."""
    dst.n += src.n
    dst.types.update(src.types)
    dst.alen += src.alen
    dst.scls.update(src.scls)
    dst.slen += src.slen
    dst.years += src.years
    dst.idigits.update(src.idigits)
    for k, sub in src.keys.items():
        _merge(dst.keys[k], sub)
    if src.items is not None:
        if dst.items is None:
            dst.items = Node()
        _merge(dst.items, src.items)


def render_node(node):
    out = []
    node.render(1, out)
    # render() emits "label: " lines followed by the value summary; join them pairwise
    lines, i = [], 0
    while i < len(out):
        if out[i].endswith(': ') and i + 1 < len(out):
            lines.append(out[i] + out[i + 1].lstrip())
            i += 2
        else:
            lines.append('  ' + out[i])
            i += 1
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('export_dir')
    ap.add_argument('--min-repeat', type=int, default=3,
                    help='a path component is shown literally only if it occurs this often (default 3)')
    args = ap.parse_args()
    root = os.path.abspath(args.export_dir)

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        comps = [] if rel == '.' else rel.split(os.sep)
        for f in filenames:
            files.append(comps + [f])

    occurrences = Counter(c for parts in files for c in parts)

    def show(c):
        return c if STRUCT_NAME.match(c) and occurrences[c] >= args.min_repeat else name_class(c)

    patterns = Counter()
    ext_count, ext_bytes = Counter(), Counter()
    depth = Counter()
    json_schemas = defaultdict(Node)
    json_errors = Counter()
    for parts in files:
        path = os.path.join(root, *parts)
        pattern = '/'.join(show(c) for c in parts)
        patterns[pattern] += 1
        depth[len(parts) - 1] += 1
        ext = os.path.splitext(parts[-1])[1].lower() or '(none)'
        ext_count[ext] += 1
        try:
            ext_bytes[ext] += os.path.getsize(path)
        except OSError:
            pass
        if ext == '.json':
            try:
                with open(path, encoding='utf-8-sig') as fh:
                    json_schemas[pattern].observe(json.load(fh))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
                json_errors[type(e).__name__] += 1

    print(f'# Structure of a Gruppwebben export ({len(files)} files)')
    print('# Values are never printed. Review before sharing.\n')
    print('## Files by type')
    for ext, n in ext_count.most_common():
        print(f'  {ext:10} {n:6} files  {ext_bytes[ext] / 1e6:9.1f} MB')
    print('\n## Directory depth of files')
    for d, n in sorted(depth.items()):
        print(f'  depth {d}: {n}')
    print('\n## Path patterns (count)')
    for p, n in patterns.most_common(60):
        print(f'  {n:6}  {p}')
    if len(patterns) > 60:
        print(f'  … {len(patterns) - 60} more patterns')
    if json_errors:
        print('\n## JSON files that could not be read: ' + ', '.join(f'{k}×{v}' for k, v in json_errors.items()))
    for pattern, node in sorted(json_schemas.items(), key=lambda kv: -kv[1].n):
        print(f'\n## JSON schema: {pattern}  ({node.n} files)')
        print(render_node(node))


if __name__ == '__main__':
    sys.exit(main())
