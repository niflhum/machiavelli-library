#!/bin/bash
# 一键入库脚本
# Usage: ./ingest.sh <源文件> <书名> <作者> <分类> <输出目录>

set -e

SRC="$1"
TITLE="$2"
AUTHOR="$3"
CATEGORY="$4"
OUTDIR="$5"

if [ $# -lt 5 ]; then
    echo "Usage: ./ingest.sh <源文件路径> <书名> <作者> <分类> <输出目录>"
    echo "  分类: machiavelli | biography | scholarship | fiction"
    echo "示例:"
    echo "  ./ingest.sh /path/to/book.txt '君主论' '马基雅维利' machiavelli library/machiavelli/prince/"
    exit 1
fi

LIBRARY_ROOT="$(dirname "$(cd "$(dirname "$0")" && pwd)")"
FULL_OUT="$LIBRARY_ROOT/$OUTDIR"

mkdir -p "$FULL_OUT"

echo "📖 Ingesting: $TITLE by $AUTHOR"
echo "   源文件: $SRC"
echo "   分类: $CATEGORY"
echo "   输出: $FULL_OUT"
echo ""

# 检测编码
ENCODING=$(file -bI "$SRC" | cut -d= -f2 | tr '[:lower:]' '[:upper:]')
echo "   编码检测: $ENCODING"

# 如果不是 txt，先转换
EXT="${SRC##*.}"
if [ "$EXT" = "docx" ]; then
    TMP="$LIBRARY_ROOT/_tmp/ingest_$(date +%s).txt"
    textutil -convert txt -encoding UTF-8 "$SRC" -output "$TMP"
    SRC="$TMP"
    echo "   ✓ DOCX → TXT 转换完成"
fi

# 复制源文件到输出目录
cp "$SRC" "$FULL_OUT/$(basename "$SRC")"
echo "   ✓ 文件已复制到 $FULL_OUT"

# 生成 MANIFEST.md
MANIFEST="$FULL_OUT/MANIFEST.md"
echo "# $TITLE — 目录" > "$MANIFEST"
echo "" >> "$MANIFEST"
echo "- 作者: $AUTHOR" >> "$MANIFEST"
echo "- 分类: $CATEGORY" >> "$MANIFEST"
echo "- 入库日期: $(date +%Y-%m-%d)" >> "$MANIFEST"
echo "- 文件名: $(basename "$SRC")" >> "$MANIFEST"
echo "   ✓ MANIFEST.md 已生成"

echo ""
echo "✅ 入库完成！"
echo ""
echo "下一步："
echo "  1. 在 catalog/catalog.json 中添加本书元数据"
echo "  2. 运行 build-index.sh 重建索引"
echo "  3. 如需按章节拆分，使用 split-by-chapter.sh"