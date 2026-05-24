#!/usr/bin/env python3
"""批量拆分传记、研究、小说类书籍 v2 — 修复正则和文件名问题"""
import re, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = "<DOWNLOAD_DIR>"

BOOKS = [
    # 亚历山大·李：从 L610 起是正文（前面是目录）
    {
        "name": "亚历山大·李《马基雅维利》",
        "src":  "2.他人著作马基雅维利传记/马基雅维利：他的生活与时代 (索恩系列) (（英）亚历山大·李（Alexander Lee）著  唐建清译) (z-library.sk, 1lib.sk, z-lib.sk).txt",
        "out":  "library/biography/alexander-lee",
        "pat":  r"^(第[一二三四五六七八九十百]+部)\s+分\s*(.*)$",
        "groups": 2,
        "start_from_marker": 7,  # 跳过前7个(目录)，从第8个(正文第一部)开始
    },
    # 麦考米克
    {
        "name": "麦考米克《解读马基雅维利》",
        "src":  "3.他人著作马基雅维利研究/解读马基雅维利：不体面的作品、暖昧的阐释与平民主义政治的德性 (【美】约翰·麦考米克) (z-library.sk, 1lib.sk, z-lib.sk).txt",
        "out":  "library/scholarship/mccormick",
        "pat":  r"^(第[一二三四五六七八九十百]+[部卷章])\s*(.*)$",
        "groups": 2,
    },
    # 毛姆：用"一/二/三"做小节
    {
        "name": "毛姆《彼时此时》",
        "src":  "4.以马基雅维利为原型的小说/毛姆作品：彼时此时—马基雅维利在伊莫拉 (威廉·萨默赛特·毛姆 (Maugham W.S.)) (z-library.sk, 1lib.sk, z-lib.sk).txt",
        "out":  "library/fiction/maugham",
        "pat":  r"^([一二三四五六七八九十百]+)$",
        "groups": 1,
    },
]

for b in BOOKS:
    src_path = os.path.join(DOWNLOADS, b["src"])
    out_dir  = os.path.join(BASE, b["out"])

    if not os.path.exists(src_path):
        print(f"⚠ {b['name']}：文件不存在 → {src_path}")
        continue

    os.makedirs(out_dir, exist_ok=True)
    with open(src_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 收集章节标记
    markers = []
    for i, line in enumerate(lines):
        m = re.match(b["pat"], line.strip())
        if m:
            label = m.group(1)
            desc  = m.group(2) if b["groups"] >= 2 and m.lastindex and m.lastindex >= 2 else ""
            markers.append((i, label, desc))

    # 可选：跳过前 N 个（带目录的书）
    skip = b.get("start_from_marker", 0)
    if skip and len(markers) > skip:
        markers = markers[skip:]

    print(f"\n## {b['name']}（{len(lines)} 行，{len(markers)} 个标记）")

    # 去重
    seen = set()
    unique = []
    for ln, num, desc in markers:
        if num not in seen:
            seen.add(num)
            unique.append((ln, num, desc))
    markers = unique

    manifest = [f"# {b['name']} 目录\n"]
    count = 0
    for idx, (start_ln, num, desc) in enumerate(markers):
        end_ln = markers[idx + 1][0] if idx + 1 < len(markers) else len(lines)
        title = f"{num}　{desc}".strip()
        safe = re.sub(r"第|章|部|卷|篇|分", "", num).strip()
        if not safe: safe = str(idx + 1)
        fname = f"{safe}.md"
        fpath = os.path.join(out_dir, fname)

        with open(fpath, "w", encoding="utf-8") as out:
            out.write(f"# {title}\n\n")
            out.write("".join(lines[start_ln:end_ln]))

        count += 1
        manifest.append(f"| {fname} | {title} |")
        print(f"  ✓ {fname}（{end_ln - start_ln} 行）")

    with open(os.path.join(out_dir, "MANIFEST.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(manifest))
    print(f"  完成：{count} 节")

print("\n✅ 完成")