#!/usr/bin/env python3
"""拆分《佛罗伦萨史》中文 txt，按卷写入 library/machiavelli/florentine/"""
import re, os

SRC = "<DOWNLOAD_DIR>/1.马基雅维利著作/佛罗伦萨史 (尼科洛·马基雅维里) (z-library.sk, 1lib.sk, z-lib.sk).txt"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'library/machiavelli/florentine')

os.makedirs(OUT, exist_ok=True)

with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find only volume markers (not "第一章/第二章" sub-chapters)
vol_data = []
for i, line in enumerate(lines):
    s = line.strip()
    m = re.match(r'^(第[一二三四五六七八]+卷)\s*(.*)$', s)
    if m:
        vol_data.append((m.group(1), m.group(2), i))

# First copy: volumes 1-8 at lines 98, 482, 992, 1409, 1796, 2180, 2582, 2954
# Second copy starts ~line 3366 — stop before it
book_start = vol_data[0][2]  # line 98
# Find where second copy begins
second_copy = None
for vn, vd, ln in vol_data:
    if ln > 3000 and vn == "第一卷":
        second_copy = ln
        break

vol_data = [(vn, vd, ln) for vn, vd, ln in vol_data if ln < second_copy]

manifest_lines = ["# 《佛罗伦萨史》目录\n", "| 卷 | 文件 | 描述 | 行数 |", "|------|------|------|------|"]
total_lines = 0

for idx, (vol_name, vol_desc, vol_ln) in enumerate(vol_data):
    vol_chinese = re.search(r'第(.+)卷', vol_name).group(1)
    vol_num_map = {"一":"1","二":"2","三":"3","四":"4","五":"5","六":"6","七":"7","八":"8"}
    vol_num = vol_num_map[vol_chinese]
    fname = f"book{vol_num}.md"
    fpath = os.path.join(OUT, fname)

    start_ln = vol_ln
    end_ln = vol_data[idx+1][2] if idx+1 < len(vol_data) else len(lines)
    body = "".join(lines[start_ln:end_ln])

    with open(fpath, "w", encoding="utf-8") as out:
        out.write(f"# {vol_name}  {vol_desc}\n\n")
        out.write(body)

    nlines = end_ln - start_ln
    total_lines += nlines
    desc_short = vol_desc[:40] if vol_desc else ""
    manifest_lines.append(f"| 第{vol_num}卷 | {fname} | {desc_short} | {nlines} |")
    print(f"  ✓ {fname} ({nlines} 行) ← 第{vol_num}卷")

manifest_path = os.path.join(OUT, "MANIFEST.md")
with open(manifest_path, "w", encoding="utf-8") as f:
    f.write("\n".join(manifest_lines))

print(f"\n《佛罗伦萨史》拆分完成: {len(vol_data)} 卷, 共 {total_lines} 行")