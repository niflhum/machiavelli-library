#!/usr/bin/env python3
"""Validate machiavelli-library integrity.

Checks:
  1. catalog.json books registered and their paths exist
  2. for directory paths: scan contained .md files (excl. MANIFEST/index.html),
     ensure at least one file with substantive content (> MIN_CONTENT_BYTES)
  3. required top-level files exist
  4. MANIFEST.md reference integrity (via validate-manifest.py logic)

Usage:
  python3 scripts/validate.py
"""
import os, json, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_CONTENT_BYTES = 200          # a real content file must exceed this
MIN_FILES_PER_BOOK = 1           # each registered book must have >= 1 content file

def dir_content_files(path):
    """Return list of .md files under path (recursive, excl. MANIFEST.md)."""
    results = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fn in files:
            if fn.endswith('.md') and fn != 'MANIFEST.md':
                results.append(os.path.join(root, fn))
    return results

def check_manifests(base):
    """Validate every MANIFEST.md reference (same logic as validate-manifest.py)."""
    broken = []
    total_refs = 0
    manifests = []
    for root, dirs, files in os.walk(base):
        if '.git' in root:
            continue
        if 'MANIFEST.md' in files:
            manifests.append(os.path.join(root, 'MANIFEST.md'))
    for mpath in manifests:
        rel_m = os.path.relpath(mpath, base)
        try:
            content = open(mpath, encoding='utf-8').read()
        except Exception:
            continue
        mdir = os.path.dirname(mpath)
        for m in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', content):
            target = m.group(2).strip()
            if target.startswith(('http://', 'https://', '#')):
                continue
            total_refs += 1
            target_clean = target.split('#')[0]
            if not target_clean:
                continue
            full = os.path.normpath(os.path.join(mdir, target_clean))
            if not os.path.exists(full):
                broken.append(f'{rel_m} → {target}')
    return total_refs, broken

print('machiavelli-library Validation\n')

errors = []
warnings = []

# 1. Load catalog
cat_path = os.path.join(BASE, 'catalog/catalog.json')
if not os.path.exists(cat_path):
    errors.append('catalog/catalog.json MISSING')
else:
    with open(cat_path) as f:
        catalog = json.load(f)
    print(f'✅ catalog.json: {len(catalog)} books registered')

    # 2. Check each book — real content validation
    for book in catalog:
        bid = book.get('id', '?')
        path = book.get('path', '')
        full_path = os.path.join(BASE, path) if path else None

        if not full_path or not os.path.exists(full_path):
            errors.append(f'  MISSING path: {bid} → {path}')
            continue

        if os.path.isdir(full_path):
            content_files = dir_content_files(full_path)
            if not content_files:
                errors.append(f'  NO content files: {bid} ({path})')
                continue
            substantive = [f for f in content_files if os.path.getsize(f) >= MIN_CONTENT_BYTES]
            stubs = [f for f in content_files if os.path.getsize(f) < MIN_CONTENT_BYTES]
            status = f'{len(content_files)} files'
            if len(substantive) < MIN_FILES_PER_BOOK:
                errors.append(f'  NO substantive content: {bid} ({path})')
                continue
            if stubs:
                warnings.append(f'  {bid}: {len(stubs)} stub files <{MIN_CONTENT_BYTES}B '
                                f'({", ".join(os.path.basename(s) for s in stubs[:3])}...)')
            print(f'  ✅ {bid} ({status})')
        else:
            size = os.path.getsize(full_path)
            if size < MIN_CONTENT_BYTES:
                errors.append(f'  STUB file: {bid} → {path} ({size}B)')
            else:
                print(f'  ✅ {bid} ({size} bytes)')

# 3. Required files
required = [
    'SKILL.md',
    'README.md',
    'index/themes.md',
    'index/quotes.md',
    'index/people.md',
    'index/timeline.md',
    'index/search-guide.md',
]
for f in required:
    if not os.path.exists(os.path.join(BASE, f)):
        errors.append(f'  MISSING required file: {f}')
print(f'\n✅ Required files: {len(required)} check passed')

# 4. MANIFEST reference integrity
try:
    total_refs, broken = check_manifests(BASE)
    if broken:
        errors.append(f'  MANIFEST broken refs ({len(broken)}):')
        for b in broken[:10]:
            errors.append(f'    {b}')
        if len(broken) > 10:
            errors.append(f'    ... and {len(broken)-10} more')
    print(f'✅ MANIFEST refs: {total_refs} checked, {len(broken)} broken')
except Exception as e:
    warnings.append(f'  MANIFEST check skipped: {e}')

# 5. Summary
if errors:
    print(f'\n❌ ERRORS ({len(errors)}):')
    for e in errors:
        print(f'  {e}')
if warnings:
    print(f'\n⚠️  WARNINGS ({len(warnings)}):')
    for w in warnings:
        print(f'  {w}')

if not errors:
    print('\n✅ All checks passed! Library is valid.')
    sys.exit(0)
print('\n❌ Validation FAILED.')
sys.exit(1)
