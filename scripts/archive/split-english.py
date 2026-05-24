#!/usr/bin/env python3
"""Split English Machiavelli texts from Project Gutenberg into chapters."""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def split_gutenberg(src_path, out_dir, chap_pattern, strip_front_matter=True):
    """Generic Gutenberg text splitter.
    
    src_path: path to downloaded English text
    out_dir: output directory
    chap_pattern: regex to match chapter headings
    strip_front_matter: skip text before first chapter marker
    """
    os.makedirs(out_dir, exist_ok=True)
    with open(src_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find chapter markers
    chapters = []
    for i, line in enumerate(lines):
        m = re.search(chap_pattern, line.strip())
        if m:
            chapters.append((i, line.strip(), m))

    if strip_front_matter and chapters:
        first_ch = chapters[0][0]
        chapters = [(ch[0], ch[1], ch[2]) for ch in chapters if ch[0] >= first_ch]
        # Drop the first (it's the chapter title itself)
        if len(chapters) > 1:
            chapters = chapters[1:]

    print(f"  Found {len(chapters)} chapter markers")

    for idx, (start_ln, title, match) in enumerate(chapters):
        end_ln = chapters[idx + 1][0] if idx + 1 < len(chapters) else len(lines)
        ch_num = match.group(1) if match.lastindex and match.lastindex >= 1 else str(idx + 1)
        try:
            ch_num = int(ch_num)
            fname = f"{ch_num:02d}-ch{ch_num}.md"
        except:
            fname = f"{ch_num}-chapter.md"

        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as out:
            out.write(f"# {title}\n\n")
            out.write("".join(lines[start_ln:end_ln]))

# Process each English text
files = [
    ("_tmp/prince-en.txt", "library/machiavelli/prince/en/", r'CHAPTER\s+([IVX]+|(\d+))'),
    ("_tmp/discourses-en.txt", "library/machiavelli/discourses/en/", r'(BOOK\s+[IVX]+|CHAPTER\s+([IVX]+|(\d+)))'),
    ("_tmp/florentine-en.txt", "library/machiavelli/florentine/en/", r'(BOOK\s+[IVX]+|CHAPTER\s+([IVX]+|(\d+)))'),
    ("_tmp/art-of-war-en.txt", "library/machiavelli/art-of-war/en/", r'(BOOK\s+[IVX]+|CHAPTER\s+([IVX]+|(\d+)))'),
]

for rel_src, rel_out, pattern in files:
    print(f"\n## {rel_src} → {rel_out}")
    split_gutenberg(os.path.join(BASE, rel_src), os.path.join(BASE, rel_out), pattern)

print("\n✓ English texts split complete")