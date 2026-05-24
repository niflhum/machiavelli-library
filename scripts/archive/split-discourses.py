#!/usr/bin/env python3
"""拆分《论李维》中文 txt，按卷/章写入 library/machiavelli/discourses/"""
import re, os

SRC = "<DOWNLOAD_DIR>/1.马基雅维利著作/论李维 (【意大利】尼科洛·马基雅维利) (z-library.sk, 1lib.sk, z-lib.sk).txt"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'library/machiavelli/discourses')

with open(SRC, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find volume markers and chapter markers (only from line 16927 onwards — where text starts)
markers = []
for i, line in enumerate(lines):
    if i < 16926: continue  # skip front matter (lines 1-16926)
    s = line.strip()
    m_vol = re.match(r'^(第[一二三]卷)$', s)
    m_ch  = re.match(r'^(第[一二三四五六七八九十百]+章)\s*(.*)$', s)
    if m_vol:
        markers.append(('volume', m_vol.group(1), i))
    elif m_ch:
        markers.append(('chapter', m_ch.group(1), m_ch.group(2), i))

vol_map = {"第一卷": "book1", "第二卷": "book2", "第三卷": "book3"}
current_dir = None
current_vol = None
chapter_count = {"book1": 0, "book2": 0, "book3": 0}
manifest_lines = ["# 《论李维》目录\n"]

for idx, m in enumerate(markers):
    if m[0] == 'volume':
        vol_name = m[1]
        current_dir = os.path.join(OUT, vol_map[vol_name])
        current_vol = vol_name
        os.makedirs(current_dir, exist_ok=True)
        manifest_lines.append(f"\n## {vol_name}\n")
        print(f"  ── {vol_name} ──")

    elif m[0] == 'chapter' and current_dir:
        ch_num = m[1]  # e.g. "第一章"
        ch_desc = m[2]  # e.g. "城邦的一般起源；罗马的起源"
        ch_title = f"{ch_num}　{ch_desc}".strip()
        start_ln = m[3]

        # Find end: next marker's line (or EOF)
        end_ln = markers[idx+1][-1] if idx+1 < len(markers) else len(lines)

        # Clean chapter number for filename
        ch_safe = ch_num.replace('第', '').replace('章', '')
        fname = f"{ch_safe}-{ch_num}.md"
        fpath = os.path.join(current_dir, fname)
        with open(fpath, "w", encoding="utf-8") as out:
            out.write(f"# {ch_title}\n\n")
            out.write("".join(lines[start_ln:end_ln]))

        chapter_count[vol_map[current_vol]] += 1
        manifest_lines.append(f"| `{vol_map[current_vol]}/{fname}` | {ch_title} |")

# Write MANIFEST
manifest_path = os.path.join(OUT, "MANIFEST.md")
with open(manifest_path, "w", encoding="utf-8") as f:
    f.write("\n".join(manifest_lines))

print(f"\n《论李维》拆分完成:")
for k in ["book1", "book2", "book3"]:
    print(f"  {k}: {chapter_count[k]} 章")
total = sum(chapter_count.values())
print(f"  MANIFEST.md 已写入")
print(f"  ⚠ 总计 {total} 章（预期 ~142 章）")