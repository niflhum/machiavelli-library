#!/usr/bin/env python3
"""
Split Machiavelli texts into chapters.
Run: python3 scripts/split-texts.py
"""

import os, re, json, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = '/Users/niko/Downloads/machiavellian'
TMP = os.path.join(BASE, '_tmp')

def read(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return len(content)

def split_by_chapter(text, pattern, max_chapters=50):
    """Split text by chapter markers. Returns list of (chapter_num, chapter_text)."""
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    if not matches:
        return [(1, text)]
    
    chapters = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        ch_num = i + 1
        ch_text = text[start:end].strip()
        chapters.append((ch_num, ch_text))
        if ch_num >= max_chapters:
            break
    return chapters

def clean_gutenberg(text):
    """Remove Project Gutenberg headers/footers."""
    # Find start of actual text (after *** START)
    start = re.search(r'\*\*\*\s*START.*?\*\*\*\s*', text, re.IGNORECASE)
    # Find end (before *** END)
    end = re.search(r'\*\*\*\s*END', text, re.IGNORECASE)
    
    if start and end:
        return text[start.end():end.start()].strip()
    elif start:
        return text[start.end():].strip()
    elif end:
        return text[:end.start()].strip()
    return text

# ============================================================
# STEP 1: Split Prince (君主论)
# ============================================================
print('=== Splitting Prince (君主论) ===')

prince_cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/君主论 (马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
prince_out = os.path.join(BASE, 'library/machiavelli/prince')

# Chinese: pattern "第X章" (Chinese or Arabic numbers)
pattern_cn = r'(?:^|\n)\s*第\s*([0-9０-９一二三四五六七八九十百]+)\s*章'
chapters = split_by_chapter(prince_cn, pattern_cn, 30)

manifest = ['# 君主论 — 目录 / The Prince — Table of Contents\n']
for num, text in chapters:
    fname = f'{num:02d}-ch{num:02d}.md'
    fpath = os.path.join(prince_out, fname)
    write(fpath, f'# 君主论 第{num}章\n\n{text}\n')
    manifest.append(f'- [第{num}章]({fname})')
    print(f'  ✅ Ch.{num}: {len(text)} chars')

write(os.path.join(prince_out, 'MANIFEST.md'), '\n'.join(manifest))
print(f'  ✅ Prince CN: {len(chapters)} chapters → {prince_out}')

# English: clean and split
prince_en = read(os.path.join(TMP, 'prince-en.txt'))
prince_en = clean_gutenberg(prince_en)
prince_en_out = os.path.join(prince_out, 'en')

# Pattern: "CHAPTER I." or "CHAPTER 1."
pattern_en = r'(?:^|\n)\s*CHAPTER\s+([IVX]+|[0-9]+)\.'
en_chapters = split_by_chapter(prince_en, pattern_en, 30)

en_manifest = ['# The Prince — Table of Contents\n']
for i, (num, text) in enumerate(en_chapters, 1):
    fname = f'{i:02d}-ch{i:02d}.md'
    fpath = os.path.join(prince_en_out, fname)
    write(fpath, f'# The Prince — Chapter {i}\n\n{text}\n')
    en_manifest.append(f'- [Chapter {i}]({fname})')
    print(f'  ✅ Prince EN Ch.{i}: {len(text)} chars')

write(os.path.join(prince_en_out, 'MANIFEST.md'), '\n'.join(en_manifest))
print(f'  ✅ Prince EN: {len(en_chapters)} chapters → {prince_en_out}')

# ============================================================
# STEP 2: Split Discourses (论李维)
# ============================================================
print('\n=== Splitting Discourses (论李维) ===')

discourses_cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/论李维 (【意大利】尼科洛·马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt'))

# Find book boundaries first
book_pattern = r'(?:^|\n)\s*第\s*([一二三四])[卷部]\s*'
books = list(re.finditer(book_pattern, discourses_cn))
if not books:
    # Try Arabic: 第一卷, 第二卷
    book_pattern = r'(?:^|\n)\s*第\s*([0-9]+)\s*卷\s*'
    books = list(re.finditer(book_pattern, discourses_cn))

print(f'  Found {len(books)} books')
discourses_out = os.path.join(BASE, 'library/machiavelli/discourses')

for bi, bm in enumerate(books):
    book_num = bi + 1
    book_start = bm.start()
    book_end = books[bi+1].start() if bi+1 < len(books) else len(discourses_cn)
    book_text = discourses_cn[book_start:book_end]
    
    # Split this book into chapters
    ch_pattern = r'(?:^|\n)\s*第\s*([0-9０-９一二三四五六七八九十]+)\s*章'
    ch_matches = list(re.finditer(ch_pattern, book_text))
    
    book_dir = os.path.join(discourses_out, f'book{book_num}')
    manifest = [f'# 论李维 第{book_num}卷 — 目录\n']
    
    for ci, cm in enumerate(ch_matches):
        ch_num = ci + 1
        ch_start = cm.start()
        ch_end = ch_matches[ci+1].start() if ci+1 < len(ch_matches) else len(book_text)
        ch_text = book_text[ch_start:ch_end].strip()
        
        fname = f'{ch_num:02d}-ch{ch_num:02d}.md'
        fpath = os.path.join(book_dir, fname)
        write(fpath, f'# 论李维 第{book_num}卷 第{ch_num}章\n\n{ch_text}\n')
        manifest.append(f'- 第{ch_num}章')
        print(f'  ✅ Discourses B{book_num} Ch.{ch_num}: {len(ch_text)} chars')
    
    write(os.path.join(book_dir, 'MANIFEST.md'), '\n'.join(manifest))

print(f'  ✅ Discourses CN: → {discourses_out}')

# ============================================================
# STEP 3: Split Florentine History (佛罗伦萨史)
# ============================================================
print('\n=== Splitting Florentine History (佛罗伦萨史) ===')

hist = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/佛罗伦萨史 (尼科洛·马基雅维里) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
hist_out = os.path.join(BASE, 'library/machiavelli/florentine')

# Pattern: 第X章 or 第X卷
chapters = split_by_chapter(hist, pattern_cn, 50)

manifest = ['# 佛罗伦萨史 — 目录\n']
for num, text in chapters:
    fname = f'book{num:02d}.md'
    fpath = os.path.join(hist_out, fname)
    write(fpath, f'# 佛罗伦萨史 第{num}卷\n\n{text}\n')
    manifest.append(f'- [第{num}卷]({fname})')
    print(f'  ✅ Florentine B{num}: {len(text)} chars')

write(os.path.join(hist_out, 'MANIFEST.md'), '\n'.join(manifest))
print(f'  ✅ Florentine: {len(chapters)} books → {hist_out}')

# ============================================================
# STEP 4: Split Art of War (兵法)
# ============================================================
print('\n=== Splitting Art of War (兵法) ===')

aow = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/君主及其战争技艺——马基雅维利《兵法》发微 (娄林张培均译) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
aow_out = os.path.join(BASE, 'library/machiavelli/art-of-war')

# The file has 娄林张培均's commentary. Need to find original Art of War sections.
# Pattern: 第X卷 or 卷X
pattern_juan = r'(?:^|\n)\s*第\s*([0-9０-９一二三四五六七])[卷篇]'
juan_matches = list(re.finditer(pattern_juan, aow))

if juan_matches:
    print(f'  Found {len(juan_matches)} juan/volumes')
    manifest = ['# 兵法 — 目录\n']
    for ji, jm in enumerate(juan_matches):
        j_num = ji + 1
        j_start = jm.start()
        j_end = juan_matches[ji+1].start() if ji+1 < len(juan_matches) else len(aow)
        j_text = aow[j_start:j_end].strip()
        
        fname = f'book{j_num}.md'
        fpath = os.path.join(aow_out, fname)
        write(fpath, f'# 兵法 第{j_num}卷\n\n{j_text}\n')
        manifest.append(f'- [第{j_num}卷]({fname})')
        print(f'  ✅ Art of War Vol.{j_num}: {len(j_text)} chars')
    
    write(os.path.join(aow_out, 'MANIFEST.md'), '\n'.join(manifest))
else:
    # Fallback: save as single file
    write(os.path.join(aow_out, 'art-of-war-full.md'), f'# 兵法\n\n{aow}\n')
    print(f'  ⚠️  No volume markers found, saved as single file')

print(f'  ✅ Art of War → {aow_out}')

# ============================================================
# STEP 5: Split Letters (书信集)
# ============================================================
print('\n=== Splitting Letters (书信集) ===')

letters_upper = read(os.path.join(TMP, 'letters-upper.txt'))
letters_lower = read(os.path.join(TMP, 'letters-lower.txt'))
letters_out = os.path.join(BASE, 'library/machiavelli/letters')

# Find year markers: 14XX年 or 15XX年
year_pattern = r'(?:^|\n)\s*(14[0-9]{2}|15[0-9]{2})\s*年'
all_letters = letters_upper + '\n\n=== 下册 ===\n\n' + letters_lower
year_matches = list(re.finditer(year_pattern, all_letters))

if year_matches:
    print(f'  Found {len(year_matches)} year markers')
    # Group by year ranges
    manifest = ['# 书信集 — 目录（按年份）\n']
    
    current_year = None
    current_text = []
    letters_by_year = {}  # {year: text}
    
    for i, ym in enumerate(year_matches):
        year = int(ym.group(1))
        start = ym.start()
        end = year_matches[i+1].start() if i+1 < len(year_matches) else len(all_letters)
        year_text = all_letters[start:end]
        
        if year not in letters_by_year:
            letters_by_year[year] = []
        letters_by_year[year].append(year_text)
    
    # Save by year ranges
    year_ranges = [(1498, 1504), (1505, 1509), (1510, 1513), (1513, 1527)]
    for ys, ye in year_ranges:
        fname = f'{ys}-{ye}.md'
        fpath = os.path.join(letters_out, fname)
        texts = []
        for y in range(ys, ye+1):
            if y in letters_by_year:
                texts.extend(letters_by_year[y])
        content = f'# 书信集 {ys}-{ye}\n\n' + '\n\n---\n\n'.join(texts) + '\n'
        write(fpath, content)
        manifest.append(f'- [{ys}-{ye}]({fname})')
        print(f'  ✅ Letters {ys}-{ye}: {len(content)} chars')
    
    write(os.path.join(letters_out, 'MANIFEST.md'), '\n'.join(manifest))
else:
    # Fallback
    write(os.path.join(letters_out, 'letters-full.md'), f'# 书信集\n\n{all_letters}\n')
    print(f'  ⚠️  No year markers found, saved as single file')

print(f'  ✅ Letters → {letters_out}')

# ============================================================
# STEP 6: Split Diplomatic Works (政务与外交著作)
# ============================================================
print('\n=== Splitting Diplomatic Works (政务与外交著作) ===')

dip_upper = read(os.path.join(TMP, 'diplomatic-upper.txt'))
dip_lower = read(os.path.join(TMP, 'diplomatic-lower.txt'))
dip_out = os.path.join(BASE, 'library/machiavelli/diplomatic')

# These are collections of works. Find work boundaries.
# Pattern: 论xxx or 关于xxx or chapter-like markers
# For now, save as upper/lower
upper_out = os.path.join(dip_out, 'upper')
lower_out = os.path.join(dip_out, 'lower')

write(os.path.join(upper_out, 'diplomatic-upper-full.md'), f'# 政务与外交著作（上册）\n\n{dip_upper}\n')
write(os.path.join(lower_out, 'diplomatic-lower-full.md'), f'# 政务与外交著作（下册）\n\n{dip_lower}\n')

print(f'  ✅ Diplomatic: saved as upper/lower → {dip_out}')

# ============================================================
# DONE
# ============================================================
print('\n✅ All texts split successfully!')
print(f'Check output in: {BASE}/library/machiavelli/')
