#!/usr/bin/env python3
"""P4: 新书入库 — 用兵之道替换 + 政务外交替换 + 4本新书拆分"""
import os, re, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(BASE, '_tmp')
LIB = os.path.join(BASE, 'library')

os.makedirs(TMP, exist_ok=True)

def read(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def split_by_pattern(text, pattern, max_chunks=100, skip_first=True):
    """Split text by regex pattern. Returns list of (index, chunk_text)."""
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    if not matches:
        # Try simpler pattern
        matches = list(re.finditer(r'(?:^|\n)(第\s*[0-9]+[章节卷篇])', text))
    if not matches:
        return []

    chunks = []
    start_idx = 1 if skip_first else 0
    for i in range(start_idx, len(matches)):
        start = matches[i].start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        chunks.append((i - start_idx + 1, text[start:end].strip()))
        if len(chunks) >= max_chunks:
            break
    return chunks

# ============================================================
# P4.1: 用兵之道替换
# ============================================================
print('=== P4.1 用兵之道替换 ===')
aow_txt = read(os.path.join(TMP, 'art-of-war-new.txt'))
aow_dir = os.path.join(LIB, 'machiavelli/art-of-war')

# Backup old art-of-war
old_aow = os.path.join(aow_dir, 'art-of-war-cn-full.md')
if os.path.exists(old_aow):
    shutil.move(old_aow, os.path.join(TMP, 'art-of-war-old-backup.md'))
    print('  📦 旧版已备份到 _tmp/')

# Save new full text
write(os.path.join(aow_dir, 'art-of-war-cn.md'), f'# 兵法（用兵之道）\n\n{aow_txt.strip()}\n')
print(f'  ✅ 用兵之道已入库 ({len(aow_txt)} chars)')

# Try splitting by 卷
pattern = r'(?:^|\n)\s*第\s*([一二三四五六七])[卷册]'
vols = split_by_pattern(aow_txt, pattern, max_chunks=10, skip_first=False)
if vols:
    cnt = 0
    manifest = ['# 用兵之道 — 目录\n']
    for vnum, vtext in vols:
        fname = f'book{vnum:02d}.md'
        write(os.path.join(aow_dir, fname), f'# 用兵之道 第{vnum}卷\n\n{vtext}\n')
        manifest.append(f'- [第{vnum}卷]({fname})')
        cnt += 1
        print(f'  ✅ 第{vnum}卷: {len(vtext)} chars')
    write(os.path.join(aow_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  📁 用兵之道: {cnt} 卷拆分完成')
else:
    print('  ⚠️  未找到卷标记，保留全文本')

# ============================================================
# P4.2: 政务与外交著作替换
# ============================================================
print('\n=== P4.2 政务与外交著作替换 ===')
dip_dir = os.path.join(LIB, 'machiavelli/diplomatic')

# Replace upper
dip_upper = read(os.path.join(TMP, 'diplomatic-upper-new.txt'))
upper_dir = os.path.join(dip_dir, 'upper')
os.makedirs(upper_dir, exist_ok=True)
write(os.path.join(upper_dir, 'diplomatic-upper.md'), f'# 政务与外交著作（上册）\n\n{dip_upper}\n')
print(f'  ✅ 政务上: {len(dip_upper)} chars')

# Replace lower
dip_lower = read(os.path.join(TMP, 'diplomatic-lower-new.txt'))
lower_dir = os.path.join(dip_dir, 'lower')
os.makedirs(lower_dir, exist_ok=True)
write(os.path.join(lower_dir, 'diplomatic-lower.md'), f'# 政务与外交著作（下册）\n\n{dip_lower}\n')
print(f'  ✅ 政务下: {len(dip_lower)} chars')

# Try to find work boundaries in upper/lower for splitting
works_pattern = r'(?:^|\n)(论\s*\S{2,10}|关于\s*\S{2,10}|致\s*\S{2,10}|出使\s*\S{2,10})'
for vol_name, vol_text, out_subdir in [
    ('upper', dip_upper, 'upper'),
    ('lower', dip_lower, 'lower')
]:
    works = list(re.finditer(works_pattern, vol_text))
    if len(works) > 3:
        out = os.path.join(dip_dir, out_subdir)
        manifest = [f'# 政务与外交著作（{vol_name}）— 目录\n']
        for i, w in enumerate(works):
            start = w.start()
            end = works[i+1].start() if i+1 < len(works) else len(vol_text)
            title = w.group(0).strip()[:30].replace('/', '-')
            fname = f'{i+1:02d}-{title}.md'
            write(os.path.join(out, fname), f'# {title}\n\n{vol_text[start:end].strip()}\n')
            manifest.append(f'- [{title}]({fname})')
            print(f'  ✅ {vol_name}/{title}')
        write(os.path.join(out, 'MANIFEST.md'), '\n'.join(manifest))

# ============================================================
# P4.3: 戏剧·诗歌·散文
# ============================================================
print('\n=== P4.3 戏剧·诗歌·散文 ===')
drama_txt = read(os.path.join(TMP, 'drama-poetry.txt'))
drama_dir = os.path.join(LIB, 'machiavelli/drama-poetry')
os.makedirs(drama_dir, exist_ok=True)

# Search for work titles (likely separated by === or 大写标题)
# Try finding sections by looking for titles like 《曼陀罗》 《十年纪》 etc.
title_pattern = r'(?:^|\n)(《[^》]+》|第[一二三四五六七八九十]+篇|金驴记|十年纪)'
sections = list(re.finditer(title_pattern, drama_txt))
if sections:
    manifest = ['# 戏剧·诗歌·散文 — 目录\n']
    for i, s in enumerate(sections):
        start = s.start()
        end = sections[i+1].start() if i+1 < len(sections) else len(drama_txt)
        title = s.group(0).strip()[:40].replace('/', '-')
        fname = f'{i+1:02d}-{title}.md'
        write(os.path.join(drama_dir, fname), f'# {title}\n\n{drama_txt[start:end].strip()}\n')
        manifest.append(f'- [{title}]({fname})')
        print(f'  ✅ {title}')
    write(os.path.join(drama_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  📁 戏剧·诗歌·散文: {len(sections)} 篇目')
else:
    write(os.path.join(drama_dir, 'drama-poetry-full.md'), f'# 戏剧·诗歌·散文\n\n{drama_txt}\n')
    print(f'  ⚠️ 无法拆分，保留全文本 ({len(drama_txt)} chars)')
    write(os.path.join(drama_dir, 'MANIFEST.md'), '# 戏剧·诗歌·散文 — 目录\n\n- [全文](drama-poetry-full.md)')

# ============================================================
# P4.4: 尼科洛的微笑
# ============================================================
print('\n=== P4.4 尼科洛的微笑 ===')
viroli_txt = read(os.path.join(TMP, 'viroli-smile.txt'))
viroli_dir = os.path.join(LIB, 'biography/viroli-smile')
os.makedirs(viroli_dir, exist_ok=True)

ch_pattern = r'(?:^|\n)\s*第\s*([0-9一二三四五六七八九十百]+)\s*章'
chapters = split_by_pattern(viroli_txt, ch_pattern, max_chunks=50, skip_first=False)
if chapters:
    manifest = ['# 尼科洛的微笑 — 目录\n']
    for cnum, ctext in chapters:
        fname = f'{cnum:02d}-ch{cnum:02d}.md'
        write(os.path.join(viroli_dir, fname), f'# 第{cnum}章\n\n{ctext}\n')
        manifest.append(f'- [第{cnum}章]({fname})')
        print(f'  ✅ 第{cnum}章: {len(ctext)} chars')
    write(os.path.join(viroli_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  📁 尼科洛的微笑: {len(chapters)} 章')
else:
    write(os.path.join(viroli_dir, 'viroli-smile-full.md'), f'# 尼科洛的微笑\n\n{viroli_txt}\n')
    write(os.path.join(viroli_dir, 'MANIFEST.md'), '# 尼科洛的微笑 — 目录\n\n- [全文](viroli-smile-full.md)')
    print(f'  ⚠️ 无法拆分 ({len(viroli_txt)} chars)')

# ============================================================
# P4.5: 权力与欲望
# ============================================================
print('\n=== P4.5 权力与欲望 ===')
najemy_txt = read(os.path.join(TMP, 'najemy-power.txt'))
najemy_dir = os.path.join(LIB, 'scholarship/najemy-power')
os.makedirs(najemy_dir, exist_ok=True)

# Pattern: 第X章
chapters = split_by_pattern(najemy_txt, ch_pattern, max_chunks=20, skip_first=False)
if chapters:
    manifest = ['# 权力与欲望 — 目录\n']
    for cnum, ctext in chapters:
        fname = f'{cnum:02d}-ch{cnum:02d}.md'
        title = ctext[:50].split('\n')[0].strip().replace('/', '-')
        write(os.path.join(najemy_dir, fname), f'# 第{cnum}章\n\n{ctext}\n')
        manifest.append(f'- [第{cnum}章]({fname})')
        print(f'  ✅ 第{cnum}章: {len(ctext)} chars')
    write(os.path.join(najemy_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  📁 权力与欲望: {len(chapters)} 章')
else:
    write(os.path.join(najemy_dir, 'najemy-power-full.md'), f'# 权力与欲望\n\n{najemy_txt}\n')
    write(os.path.join(najemy_dir, 'MANIFEST.md'), '# 权力与欲望 — 目录\n\n- [全文](najemy-power-full.md)')
    print(f'  ⚠️ 无法拆分 ({len(najemy_txt)} chars)')

# ============================================================
# P4.6: Strauss - Thoughts on Machiavelli
# ============================================================
print('\n=== P4.6 Thoughts on Machiavelli ===')
strauss_txt = read(os.path.join(TMP, 'strauss-thoughts.txt'))
strauss_dir = os.path.join(LIB, 'scholarship/strauss-thoughts')
os.makedirs(strauss_dir, exist_ok=True)

# Remove Gutenberg/OCR headers
# Find Introduction marker
intro_m = re.search(r'\n\s*(Introduction|INTRODUCTION)\s*\n', strauss_txt)
if intro_m:
    strauss_txt = strauss_txt[intro_m.start():]

# English chapter pattern
en_ch_pattern = r'(?:^|\n)\s*(Chapter|CHAPTER)\s+([IVXL]+|[0-9]+)\b'
chapters = split_by_pattern(strauss_txt, en_ch_pattern, max_chunks=20, skip_first=False)
if chapters and len(chapters) >= 3:
    manifest = ['# Thoughts on Machiavelli — Table of Contents\n']
    for cnum, ctext in chapters:
        fname = f'{cnum:02d}-ch{cnum:02d}.md'
        write(os.path.join(strauss_dir, fname), f'# Chapter {cnum}\n\n{ctext}\n')
        manifest.append(f'- [Chapter {cnum}]({fname})')
        print(f'  ✅ Ch.{cnum}: {len(ctext)} chars')
    write(os.path.join(strauss_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  📁 Strauss: {len(chapters)} chapters')
else:
    write(os.path.join(strauss_dir, 'strauss-thoughts-full.md'), f'# Thoughts on Machiavelli\n\n{strauss_txt}\n')
    write(os.path.join(strauss_dir, 'MANIFEST.md'), '# Thoughts on Machiavelli — TOC\n\n- [Full text](strauss-thoughts-full.md)')
    print(f'  ⚠️ 无法拆分 ({len(strauss_txt)} chars)')

print('\n✅ P4 完成！')
