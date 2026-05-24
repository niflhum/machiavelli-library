#!/bin/bash
# P1.3: 批量去硬编码。将绝对路径替换为动态路径推导。

set -e
SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
LIBRARY_ROOT="$(dirname "$SCRIPTS_DIR")"

cd "$SCRIPTS_DIR"

echo "=== P1.3 脚本去硬编码 ==="
echo "  脚本目录: $SCRIPTS_DIR"
echo "  图书馆根: $LIBRARY_ROOT"
echo ""

# Python 文件: 替换 BASE = '...' 为动态推导
for f in \
    split-texts.py \
    split-all.py \
    split-prince.py \
    split-books.py \
    split-english.py \
    split-english-v2.py \
    ; do
    if [ -f "$f" ]; then
        sed -i '' "s|^BASE = .*|BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))|" "$f"
        echo "  ✅ $f"
    fi
done

# split-discourses.py: 特殊处理（OUT 路径）
if [ -f "split-discourses.py" ]; then
    sed -i '' "s|^OUT = .*|OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'library/machiavelli/discourses')|" split-discourses.py
    echo "  ✅ split-discourses.py"
fi

# split-florentine.py: 特殊处理
if [ -f "split-florentine.py" ]; then
    sed -i '' "s|^OUT = .*|OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'library/machiavelli/florentine')|" split-florentine.py
    echo "  ✅ split-florentine.py"
fi

# Shell 文件
for f in ingest.sh validate.sh; do
    if [ -f "$f" ]; then
        sed -i '' 's|^LIBRARY_ROOT=.*|LIBRARY_ROOT="$(dirname "$(cd "$(dirname "$0")" \&\& pwd)")"|' "$f"
        echo "  ✅ $f"
    fi
done

echo ""
echo "✅ P1.3 完成"
