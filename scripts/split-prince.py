#!/usr/bin/env python3
"""Split Prince (君主论) Chinese and English correctly."""
import os, re

BASE = '/Users/niko/Desktop/machiavelli-library'
DOWNLOADS = '/Users/niko/Downloads/machiavellian'

def read(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return len(content)

def find_body_start(text, keywords):
    """Find where the actual body text starts (after TOC, prefaces, etc.)."""
    for kw in keywords:
        idx = text.find(kw)
        if idx > 500:  # Must be after front matter
            return idx
    return 0

# ================================================================
# CN: 君主论 (拿破仑批注版, 吉林出版)
# ================================================================
print('=== Splitting Prince CN ===')
prince_cn = read(os.path.join(DOWNLOADS, '1.马基雅维利著作/君主论 (马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt'))

# Find body start: "一切国家" or "过去曾经"
body_start = find_body_start(prince_cn, ['一切国家', '过去曾经和现在正在', '一切国家、一切领地'])
print(f'  Body starts at position: {body_start}')
body_text = prince_cn[body_start:]

# Now find chapter markers in body_text
# Pattern: \n\n第X章
ch_pattern = r'\n\n第\s*([0-9０-９一二三四五六七八九十]+)\s*章\s+([^\n]{2,50})'
matches = list(re.finditer(ch_pattern, body_text))

if not matches:
    # Try simpler pattern
    ch_pattern = r'(?:^|\n)\s*第\s*([0-9]+)\s*章\s+([^\n]{2,50})'
    matches = list(re.finditer(ch_pattern, body_text))

print(f'  Found {len(matches)} chapter markers in body')

if matches:
    out_dir = os.path.join(BASE, 'library/machiavelli/prince')
    manifest = ['# 君主论 — 目录 / The Prince — Table of Contents\n']
    
    for i, m in enumerate(matches):
        ch_num_str = m.group(1)
        # Convert Chinese numbers to arabic
        ch_num = int(ch_num_str) if ch_num_str.isdigit() else {
            '一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10
        }.get(ch_num_str, i+1)
        
        start = m.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(body_text)
        ch_text = body_text[start:end].strip()
        
        fname = f'{ch_num:02d}-ch{ch_num:02d}.md'
        fpath = os.path.join(out_dir, fname)
        write(fpath, f'# 君主论 第{ch_num}章\n\n{ch_text}\n')
        manifest.append(f'- [第{ch_num}章]({fname}) — {m.group(2)[:30] if m.lastindex >= 2 else ""}')
        print(f'  ✅ Ch.{ch_num}: {len(ch_text)} chars')
    
    write(os.path.join(out_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  ✅ Prince CN: {len(matches)} chapters → {out_dir}')
else:
    # Fallback: save full body
    out_dir = os.path.join(BASE, 'library/machiavelli/prince')
    write(os.path.join(out_dir, 'prince-full.md'), f'# 君主论\n\n{body_text}\n')
    print(f'  ⚠️  No chapter markers found in body, saved as single file')

# ================================================================
# EN: The Prince (Project Gutenberg)
# ================================================================
print('\n=== Splitting Prince EN ===')
prince_en = read(os.path.join(BASE, '_tmp/prince-en.txt'))

# Clean Gutenberg headers/footers
start_marker = re.search(r'\*\*\*\s*START.*?\*\*\*', prince_en, re.IGNORECASE)
end_marker = re.search(r'\*\*\*\s*END', prince_en, re.IGNORECASE)
if start_marker:
    prince_en = prince_en[start_marker.end():]
if end_marker:
    prince_en = prince_en[:end_marker.start()]
prince_en = prince_en.strip()

# Find chapter markers: "CHAPTER I." or "CHAPTER 1."
ch_pattern_en = r'\n\s*CHAPTER\s+([IVX]+|[0-9]+)\.\s*([^\n]{2,80})'
matches_en = list(re.finditer(ch_pattern_en, prince_en, re.IGNORECASE))

print(f'  Found {len(matches_en)} chapter markers')

if matches_en:
    out_dir = os.path.join(BASE, 'library/machiavelli/prince/en')
    manifest = ['# The Prince — Table of Contents\n']
    
    for i, m in enumerate(matches_en):
        ch_num_str = m.group(1)
        # Convert Roman to arabic
        roman_map = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,
                      'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,'XVIII':18,
                      'XIX':19,'XX':20,'XXI':21,'XXII':22,'XXIII':23,'XXIV':24,'XXV':25}
        ch_num = roman_map.get(ch_num_str.upper(), i+1) if not ch_num_str.isdigit() else int(ch_num_str)
        
        start = m.start()
        end = matches_en[i+1].start() if i+1 < len(matches_en) else len(prince_en)
        ch_text = prince_en[start:end].strip()
        
        fname = f'{ch_num:02d}-ch{ch_num:02d}.md'
        fpath = os.path.join(out_dir, fname)
        write(fpath, f'# The Prince — Chapter {ch_num}\n\n{ch_text}\n')
        manifest.append(f'- [Chapter {ch_num}]({fname})')
        print(f'  ✅ Ch.{ch_num}: {len(ch_text)} chars')
    
    write(os.path.join(out_dir, 'MANIFEST.md'), '\n'.join(manifest))
    print(f'  ✅ Prince EN: {len(matches_en)} chapters → {out_dir}')
else:
    out_dir = os.path.join(BASE, 'library/machiavelli/prince/en')
    write(os.path.join(out_dir, 'prince-en-full.md'), f'# The Prince\n\n{prince_en}\n')
    print(f'  ⚠️  No chapter markers found, saved as single file')

print('\n✅ Prince split complete!')
