#!/usr/bin/env python3
"""P0.4: Organize Discourses EN chapters into book subdirectories.
Extract original Roman numeral from each chapter and assign to book based on range."""
import os, re, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_DIR = os.path.join(BASE, 'library/machiavelli/discourses/en')

def roman_to_int(s):
    """Roman numeral to integer."""
    vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    result = 0
    prev = 0
    for c in reversed(s.upper()):
        v = vals.get(c, 0)
        if v >= prev:
            result += v
        else:
            result -= v
        prev = v
    return result

# Assign book by chapter number in original Discourses
def assign_book(orig_num):
    if orig_num <= 60:
        return 1
    elif orig_num <= 93:
        return 2
    else:
        return 3

# Find original chapter numbers
chapter_mapping = []
for f in sorted(os.listdir(EN_DIR)):
    if not f.startswith('chapter-'):
        continue
    fpath = os.path.join(EN_DIR, f)
    with open(fpath, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()
    
    # Extract original Roman numeral from header like "CHAPTER XLIX."
    m = re.search(r'CHAPTER\s+([IVXLCD]+)\b', content[:500])
    if m:
        orig_num = roman_to_int(m.group(1))
        book = assign_book(orig_num)
        chapter_mapping.append((f, book, orig_num))
        print(f'  {f}: original ch.{orig_num} → Book {book}')

# Create book dirs and move files
for book in [1, 2, 3]:
    book_dir = os.path.join(EN_DIR, f'book{book}')
    os.makedirs(book_dir, exist_ok=True)

for fname, book, orig_num in chapter_mapping:
    src = os.path.join(EN_DIR, fname)
    dst = os.path.join(EN_DIR, f'book{book}', fname)
    shutil.move(src, dst)

# Move book files
for book_name in ['book-i.md', 'book-ii.md', 'book-iii.md']:
    src = os.path.join(EN_DIR, book_name)
    if os.path.exists(src):
        book_num = book_name.split('-')[1].replace('.md', '')
        book_num = {'i': 1, 'ii': 2, 'iii': 3}[book_num]
        dst = os.path.join(EN_DIR, f'book{book_num}', f'full.md')
        shutil.move(src, dst)

print(f'\n✅ P0.4 完成: {len(chapter_mapping)} 个章节分入 3 卷')
for b in [1, 2, 3]:
    count = sum(1 for _, book, _ in chapter_mapping if book == b)
    print(f'  Book {b}: {count} chapters')

# Create EN MANIFEST
manifest = ['# Discourses on Livy (EN) — Table of Contents\n']
for fname, book, orig_num in sorted(chapter_mapping, key=lambda x: (x[1], x[2])):
    manifest.append(f'- Book {book}, Ch.{orig_num}: [{fname}](book{book}/{fname})')
with open(os.path.join(EN_DIR, 'MANIFEST.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(manifest))
print('  📁 MANIFEST.md 已生成')
