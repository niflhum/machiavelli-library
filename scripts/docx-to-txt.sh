#!/bin/bash
# 批量将 DOCX 转为 TXT（使用 macOS 内置 textutil）
# Usage: ./docx-to-txt.sh <docx-file> [output-file]

set -e

if [ $# -lt 1 ]; then
    echo "Usage: ./docx-to-txt.sh <docx-file> [output-file]"
    echo "  将 DOCX 文件转为 UTF-8 编码的纯文本"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-${INPUT%.docx}.txt}"

textutil -convert txt -encoding UTF-8 "$INPUT" -output "$OUTPUT"
echo "✓ Converted: $INPUT → $OUTPUT ($(wc -c < "$OUTPUT") bytes)"