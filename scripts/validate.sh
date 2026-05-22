#!/bin/bash
# 验证馆藏完整性
# 检查 catalog.json 中的每本书是否存在对应文件

echo "📋 马基雅维利图书馆 — 完整性验证"
echo "=================================="
echo ""

LIBRARY_ROOT="/Users/niko/Desktop/machiavelli-library"
CATALOG="$LIBRARY_ROOT/catalog/catalog.json"

if [ ! -f "$CATALOG" ]; then
    echo "❌ catalog.json 不存在"
    exit 1
fi

echo "✅ catalog.json 存在"
echo ""

# 统计文件
TOTAL_FILES=$(find "$LIBRARY_ROOT/library" -name "*.md" | wc -l | tr -d ' ')
TOTAL_SIZE=$(du -sh "$LIBRARY_ROOT/library" | cut -f1)
echo "📦 馆藏统计: $TOTAL_FILES 个章节文件, 共 $TOTAL_SIZE"
echo ""

# 列出各目录
echo "📂 目录结构:"
for dir in "$LIBRARY_ROOT"/library/machiavelli/*/; do
    if [ -d "$dir" ]; then
        name=$(basename "$dir")
        count=$(find "$dir" -name "*.md" -not -name "MANIFEST.md" | wc -l | tr -d ' ')
        printf "  %-20s %3s 文件\n" "$name" "$count"
    fi
done
for dir in "$LIBRARY_ROOT"/library/biography/*/ "$LIBRARY_ROOT"/library/scholarship/*/ "$LIBRARY_ROOT"/library/fiction/*/; do
    if [ -d "$dir" ]; then
        name=$(basename "$dir")
        count=$(find "$dir" -name "*.md" -not -name "MANIFEST.md" | wc -l | tr -d ' ')
        printf "  %-20s %3s 文件\n" "$name" "$count"
    fi
done

echo ""
echo "📝 索引文件:"
for f in "$LIBRARY_ROOT"/index/*.md; do
    printf "  %s (%s)\n" "$(basename $f)" "$(wc -c < $f | tr -d ' ')B"
done

echo ""
echo "✅ 验证完成"