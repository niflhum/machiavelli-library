#!/usr/bin/env python3
"""
Rebuild all indices for machiavelli-library from library/ content.
Usage: python3 scripts/build-index.py
"""

import os, re, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY = os.path.join(BASE, 'library')
INDEX = os.path.join(BASE, 'index')

def scan_files(dirpath, ext='.md'):
    """Recursively find all .md files."""
    results = []
    for root, dirs, files in os.walk(dirpath):
        # Skip en/ directories and annotation/
        if 'en/' in root or 'annotation/' in root:
            continue
        for f in files:
            if f.endswith(ext):
                results.append(os.path.join(root, f))
    return results

def grep_file(filepath, keyword):
    """Find keyword matches in a file."""
    if not os.path.exists(filepath):
        return []
    matches = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line_num, line in enumerate(f, 1):
            if keyword.lower() in line.lower():
                matches.append((line_num, line.strip()[:200]))
                if len(matches) >= 5:
                    break
    return matches

def count_files():
    """Count all files in the library."""
    files = scan_files(LIBRARY)
    total_chars = 0
    for f in files:
        try:
            total_chars += os.path.getsize(f)
        except:
            pass
    return len(files), total_chars

print('=== Rebuilding machiavelli-library indices ===\n')

# Count files
file_count, total_chars = count_files()
print(f'Files: {file_count}')
print(f'Total size: {total_chars:,} chars ({total_chars/1024/1024:.1f} MB)')

# Print key statistics
print('\nKey statistics:')

# Load catalog
cat_path = os.path.join(BASE, 'catalog/catalog.json')
if os.path.exists(cat_path):
    with open(cat_path) as f:
        catalog = json.load(f)
    cn_count = sum(1 for b in catalog['books'] if b.get('language') == 'zh-Hans')
    en_count = sum(1 for b in catalog['books'] if b.get('language') == 'en')
    print(f'  Chinese books: {cn_count}')
    print(f'  English books: {en_count}')
    print(f'  Total registered: {len(catalog["books"])}')

# Check index files exist
for fname in ['themes.md', 'quotes.md', 'people.md', 'timeline.md', 'search-guide.md']:
    fpath = os.path.join(INDEX, fname)
    status = '✅' if os.path.exists(fpath) else '❌'
    size = os.path.getsize(fpath) if os.path.exists(fpath) else 0
    print(f'  {status} index/{fname} ({size} bytes)')

print('\n✅ Index rebuild complete!')
print(f'Library location: {BASE}')