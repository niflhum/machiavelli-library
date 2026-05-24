#!/usr/bin/env python3
"""Process correct English texts from Gutenberg into library."""
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_books(lines):
    """Find chapter markers in Gutenberg text"""
    markers = []
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'^(BOOK\s+[IVX]+|CHAPTER\s+[IVX]+)\.?\s*(.*)$', s, re.I)
        if m:
            markers.append((i, m.group(1).upper(), m.group(2)))
    return markers

# 1. Discourses on Livy (ID 10827)
print("## Discourses on Livy (EN)")
with open(f"{BASE}/_tmp/discourses-en2.txt") as f:
    lines = f.readlines()
markers = find_books(lines)
print(f"  Markers: {len(markers)}")
out_dir = f"{BASE}/library/machiavelli/discourses/en"
os.makedirs(out_dir, exist_ok=True)
# Clear old files
for f in os.listdir(out_dir):
    if f.endswith('.md'):
        os.remove(os.path.join(out_dir, f))

for idx, (start_ln, label, desc) in enumerate(markers):
    end_ln = markers[idx+1][0] if idx+1 < len(markers) else len(lines)
    fname = f"{label.lower().replace(' ','-')}.md"
    fpath = os.path.join(out_dir, fname)
    title = f"{label} {desc}".strip()
    with open(fpath, 'w') as out:
        out.write(f"# {title}\n\n")
        out.write("".join(lines[start_ln:end_ln]))
    print(f"  ✓ {fname} ({end_ln-start_ln} lines)")
print(f"  Written {len(markers)} files to {out_dir}")

# 2. Florentine History (ID 2464)
print("\n## Florentine History (EN)")
with open(f"{BASE}/_tmp/florentine-en2.txt") as f:
    lines = f.readlines()
markers = find_books(lines)
print(f"  Markers: {len(markers)}")
out_dir = f"{BASE}/library/machiavelli/florentine/en"
os.makedirs(out_dir, exist_ok=True)
# Clear old files
for f in os.listdir(out_dir):
    if f.endswith('.md'):
        os.remove(os.path.join(out_dir, f))

for idx, (start_ln, label, desc) in enumerate(markers):
    end_ln = markers[idx+1][0] if idx+1 < len(markers) else len(lines)
    fname = f"{label.lower().replace(' ','-')}.md"
    fpath = os.path.join(out_dir, fname)
    title = f"{label} {desc}".strip()
    with open(fpath, 'w') as out:
        out.write(f"# {title}\n\n")
        out.write("".join(lines[start_ln:end_ln]))
    print(f"  ✓ {fname} ({end_ln-start_ln} lines)")
print(f"  Written {len(markers)} files to {out_dir}")

# 3. Art of War from Vol I (line 34 to before The Prince at line 9274)
print("\n## The Art of War (EN) - extracting from Machiavelli Vol I")
with open(f"{BASE}/_tmp/machiavelli-vol1-en.txt") as f:
    lines = f.readlines()

# Extract Art of War: from START line (34) to THE PRINCE start (9274)
art_of_war = lines[34:9274]
# Find BOOK markers in Art of War section  
pattern = r'^(THE\s+(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH)\s+BOOK[SE]?)\s*$'
markers = []
for i, line in enumerate(art_of_war):
    m = re.match(pattern, line.strip(), re.I)
    if m:
        markers.append((i, m.group(1).upper()))

print(f"  Book markers in AoW: {len(markers)}")
out_dir = f"{BASE}/library/machiavelli/art-of-war/en"
os.makedirs(out_dir, exist_ok=True)
for f in os.listdir(out_dir):
    if f.endswith('.md'):
        os.remove(os.path.join(out_dir, f))

if markers:
    for idx, (start_ln, label) in enumerate(markers):
        end_ln = markers[idx+1][0] if idx+1 < len(markers) else len(art_of_war)
        fname = f"{label.lower().replace(' ','-')}.md"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, 'w') as out:
            out.write(f"# {label}\n\n")
            out.write("".join(art_of_war[start_ln:end_ln]))
        print(f"  ✓ {fname} ({end_ln-start_ln} lines)")
else:
    # No book markers found, save as single file
    with open(os.path.join(out_dir, "full.md"), 'w') as out:
        out.write("# The Art of War\n\n")
        out.write("".join(art_of_war))
    print(f"  ✓ full.md ({len(art_of_war)} lines)")

print(f"  Written to {out_dir}")

print("\n✅ English texts complete")