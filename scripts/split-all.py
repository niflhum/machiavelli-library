#!/usr/bin/env python3
"""
Split all Machiavelli texts into manageable files.
Saves as single full files per book for simplicity and reliability.
"""

import os, re

BASE = '/Users/niko/Desktop/machiavelli-library'
DOWNLOADS = '/Users/niko/Downloads/machiavellian'
TMP = os.path.join(BASE, '_tmp')

def read(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  ✅ {os.path.relpath(path, BASE)} ({len(content)} chars)')

def clean_gutenberg(text):
    """Remove Project Gutenberg boilerplate."""
    s = re.search(r'\*\*\*\s*START.*?\*\*\*', text, re.IGNORECASE)
    e = re.search(r'\*\*\*\s*END', text, re.IGNORECASE)
    if s and e:
        text = text[s.end():e.start()]
    elif s:
        text = text[s.end():]
    elif e:
        text = text[:e.start()]
    # Remove common header lines
    text = re.sub(r'^.*?Produced by.*?\n', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^.*?E\-?text.*?\n', '', text, flags=re.IGNORECASE)
    return text.strip()

# ============================================================
# 1. Prince (君主论) — CN + EN
# ============================================================
print('=== The Prince / 君主论 ===')

# CN: 拿破仑批注版 — find body after commentary
cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/君主论 (马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
body_start = cn.find('一切国家、一切领地')
if body_start < 0:
    body_start = cn.find('过去曾经和现在正在')
if body_start < 500:
    body_start = 0
# Trim trailing back matter (after Chapter 26 ends)
end_marker = cn.find('本书中的术语说明')
if end_marker < 0:
    end_marker = cn.find('术语说明', body_start)
if end_marker < 0:
    end_marker = cn.find('专名索引', body_start)
body = cn[body_start:end_marker if end_marker > body_start else len(cn)]
write(f'{BASE}/library/machiavelli/prince/prince-cn-full.md', f'# 君主论\n\n{body}\n')

# EN: Project Gutenberg
en = read(os.path.join(TMP, 'prince-en.txt'))
en = clean_gutenberg(en)
# Find body start (skip TOC)
en_body_start = en.find('CHAPTER I.\n\nHOW MANY')
if en_body_start < 0:
    en_body_start = en.find('How many kinds of principalities')
    # search back for CHAPTER I
    back = en[:en_body_start].rfind('CHAPTER I')
    if back > 0:
        en_body_start = back
if en_body_start < 0:
    en_body_start = 0
en_body = en[en_body_start:]
write(f'{BASE}/library/machiavelli/prince/en/prince-en-full.md', f'# The Prince\n\n{en_body}\n')

# ============================================================
# 2. Discourses on Livy (论李维) — CN + EN
# ============================================================
print('\n=== Discourses on Livy / 论李维 ===')

cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/论李维 (【意大利】尼科洛·马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt'))

# Split into 3 books + find each
book_pattern = r'(?:^|\n)\s*第\s*([一二三])\s*卷\s*'
books = list(re.finditer(book_pattern, cn))
if books:
    for bi, bm in enumerate(books):
        book_num = bi + 1
        bstart = bm.start()
        bend = books[bi+1].start() if bi+1 < len(books) else len(cn)
        btext = cn[bstart:bend].strip()
        write(f'{BASE}/library/machiavelli/discourses/book{book_num}/discourses-book{book_num}-cn.md',
              f'# 论李维 第{book_num}卷\n\n{btext}\n')
else:
    # Try to find books at higher positions (after front matter)
    for i in range(1, 4):
        pattern = f'第{i}卷'
        idx = cn.find(pattern)
        if idx >= 0:
            next_idx = cn.find(f'第{i+1}卷', idx+5) if i < 3 else len(cn)
            btext = cn[idx:min(next_idx, len(cn))].strip()
            write(f'{BASE}/library/machiavelli/discourses/book{i}/discourses-book{i}-cn.md',
                  f'# 论李维 第{i}卷\n\n{btext}\n')

# EN: Project Gutenberg
en = read(os.path.join(TMP, 'discourses-en.txt'))
en = clean_gutenberg(en)
# Find body start
en_start = en.find('FIRST BOOK')
if en_start < 0:
    en_start = 0
en_body = en[en_start:]
write(f'{BASE}/library/machiavelli/discourses/en/discourses-en-full.md', f'# Discourses on Livy\n\n{en_body}\n')

# ============================================================
# 3. Florentine History (佛罗伦萨史) — CN + EN
# ============================================================
print('\n=== Florentine History / 佛罗伦萨史 ===')

cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/佛罗伦萨史 (尼科洛·马基雅维里) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
write(f'{BASE}/library/machiavelli/florentine/florentine-cn-full.md', f'# 佛罗伦萨史\n\n{cn}\n')

en = read(os.path.join(TMP, 'florentine-en.txt'))
en = clean_gutenberg(en)
write(f'{BASE}/library/machiavelli/florentine/en/florentine-en-full.md', f'# Florentine History\n\n{en}\n')

# ============================================================
# 4. Art of War (兵法) — CN + EN
# ============================================================
print('\n=== Art of War / 兵法 ===')

cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/君主及其战争技艺——马基雅维利《兵法》发微 (娄林张培均译) (z-library.sk, 1lib.sk, z-lib.sk).txt'))
write(f'{BASE}/library/machiavelli/art-of-war/art-of-war-cn-full.md', f'# 兵法\n\n{cn}\n')

en = read(os.path.join(TMP, 'art-of-war-en.txt'))
en = clean_gutenberg(en)
write(f'{BASE}/library/machiavelli/art-of-war/en/art-of-war-en-full.md', f'# The Art of War\n\n{en}\n')

# ============================================================
# 5. Letters (书信集) — CN only
# ============================================================
print('\n=== Letters / 书信集 ===')

lu = read(os.path.join(TMP, 'letters-upper.txt'))
ll = read(os.path.join(TMP, 'letters-lower.txt'))
write(f'{BASE}/library/machiavelli/letters/letters-upper-cn.md', f'# 书信集（上册）\n\n{lu}\n')
write(f'{BASE}/library/machiavelli/letters/letters-lower-cn.md', f'# 书信集（下册）\n\n{ll}\n')

# ============================================================
# 6. Diplomatic Works (政务与外交著作) — CN only
# ============================================================
print('\n=== Diplomatic Works / 政务与外交著作 ===')

du = read(os.path.join(TMP, 'diplomatic-upper.txt'))
dl = read(os.path.join(TMP, 'diplomatic-lower.txt'))
write(f'{BASE}/library/machiavelli/diplomatic/upper/diplomatic-upper-cn.md', f'# 政务与外交著作（上册）\n\n{du}\n')
write(f'{BASE}/library/machiavelli/diplomatic/lower/diplomatic-lower-cn.md', f'# 政务与外交著作（下册）\n\n{dl}\n')

# ============================================================
# 7. Biographies + Scholarship + Fiction
# ============================================================
print('\n=== Biographies, Scholarship, Fiction ===')

biography_texts = [
    ('盐野七生《我的朋友马基雅维利》', 'salt-seven', 'salt-seven-friend-cn'),
    ('亚历山大·李《马基雅维利：他的生活与时代》', 'alexander-lee', 'alexander-lee-bio-cn'),
]
scholarship_texts = [
    ('盐野七生《马基雅维利语录》', 'salt-quotes', 'salt-quotes-cn'),
    ('约翰·麦考米克《解读马基雅维利》', 'mccormick', 'mccormick-interpretation-cn'),
]
fiction_texts = [
    ('毛姆《彼时此时——马基雅维利在伊莫拉》', 'maugham', 'maugham-thin-there-cn'),
]

for title, dirname, fname_base in biography_texts:
    match = f'{title}*.txt'
    for root, dirs, files in os.walk(DOWNLOADS):
        for f in files:
            if f.endswith('.txt') and '盐野七生' in f and dirname == 'salt-seven':
                txt = read(os.path.join(root, f))
                write(f'{BASE}/library/biography/{dirname}/{fname_base}.md', f'# {title}\n\n{txt}\n')
                break
            elif f.endswith('.txt') and '亚历山大' in f and dirname == 'alexander-lee':
                txt = read(os.path.join(root, f))
                write(f'{BASE}/library/biography/{dirname}/{fname_base}.md', f'# {title}\n\n{txt}\n')
                break

for title, dirname, fname_base in scholarship_texts:
    for root, dirs, files in os.walk(DOWNLOADS):
        for f in files:
            if f.endswith('.txt') and '语录' in f and dirname == 'salt-quotes':
                txt = read(os.path.join(root, f))
                write(f'{BASE}/library/scholarship/{dirname}/{fname_base}.md', f'# {title}\n\n{txt}\n')
                break
            elif f.endswith('.txt') and '麦考米克' in f and dirname == 'mccormick':
                txt = read(os.path.join(root, f))
                write(f'{BASE}/library/scholarship/{dirname}/{fname_base}.md', f'# {title}\n\n{txt}\n')
                break

for title, dirname, fname_base in fiction_texts:
    for root, dirs, files in os.walk(DOWNLOADS):
        for f in files:
            if f.endswith('.txt') and '毛姆' in f:
                txt = read(os.path.join(root, f))
                write(f'{BASE}/library/fiction/{dirname}/{fname_base}.md', f'# {title}\n\n{txt}\n')
                break

print('\n✅ All texts saved successfully!')