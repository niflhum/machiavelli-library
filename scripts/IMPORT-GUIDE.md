# 新书入库操作指南

本指南介绍如何将一本书（txt/epub/mobi/docx/pdf）入库到马基雅维利图书馆。

---

## 7 步入库流程

### Step 1: 准备文本文件

如果是 txt 格式 → 直接使用
如果是 docx 格式 → 运行 `./scripts/docx-to-txt.sh` 转换
如果是 epub/mobi/pdf → 先用 Calibre 或其他工具转为 txt

### Step 2: 检查文本质量

```bash
head -100 新书.txt     # 查看开头
wc -l 新书.txt          # 统计行数
file 新书.txt           # 检查编码（应为 UTF-8）
```

如果非 UTF-8（如 GBK/GB2312），使用 `iconv` 转换：
```bash
iconv -f GBK -t UTF-8 新书.txt > 新书-utf8.txt
```

### Step 3: 确定分类和目录

| 内容类型 | 分类 | 目标目录 |
|----------|------|----------|
| 马基雅维利本人著作 | machiavelli | `library/machiavelli/<著作名>/` |
| 传记 | biography | `library/biography/<作者>/` |
| 学术研究 | scholarship | `library/scholarship/<作者>/` |
| 小说 | fiction | `library/fiction/<作者>/` |

### Step 4: 按章节拆分

编写拆分脚本（可参考 `scripts/split-prince.py` 的模板），或手动拆分。
每章一个 `.md` 文件。

拆分规则（正则表达式模板）：

| 章节格式 | 正则 |
|----------|------|
| 第 X 章 | `^第[0-9一二三四五六七八九十百]+章` |
| Chapter X | `^CHAPTER\s+[IVX]+` |
| 第 X 卷 | `^第[一二三四五六七八]+卷` |
| 中文序号 | `^[一二三四五六七八九十百]+$` |

### Step 5: 生成 MANIFEST.md

```markdown
# <书名> — 目录

| 章节 | 文件 | 标题 |
|------|------|------|
| 第 1 章 | 01-ch1.md | 论… |
```

### Step 6: 更新 catalog.json

在 `catalog/catalog.json` 中添加条目：

```json
{
  "id": "<唯一标识>",
  "title": "<中文书名>",
  "author": "<作者>",
  "category": "<分类>",
  "path": "<库内路径>",
  "language": "zh",
  "chapters": <章节数>,
  "notes": "<备注>"
}
```

### Step 7: 运行验证

```bash
bash scripts/validate.sh
```

---

## 支持的格式处理

| 格式 | 工具 | 命令 |
|------|------|------|
| txt | 直接使用 | — |
| docx | textutil (macOS 内置) | `./scripts/docx-to-txt.sh` |
| epub | Calibre / pandoc | `ebook-convert file.epub file.txt` |
| pdf | pdftotext | `pdftotext -layout file.pdf` |

---

## 常见问题

### OCR 错误处理

如果是 OCR 来源的文本（如扫描件转换），在文件中标注：
```html
<!-- OCR疑似错误：[原文] -->
```

### 编码问题

```bash
file -bI 文件名          # 检查编码
iconv -f 原编码 -t UTF-8  # 转换
```

### 重复章节

部分 txt 文件包含两份副本（目录 + 正文），只取正文部分。
检查章节标记间的间隔：目录版通常每章仅几行，正文版每章数百行。

---

## 参考文献拆分脚本

已有拆分脚本：
- `split-prince.py` — 君主论（处理双份副本）
- `split-discourses.py` — 论李维（卷/章双层结构）
- `split-florentine.py` — 佛罗伦萨史
- `split-books.py` — 传记/研究/小说通用拆分
- `split-english.py` — 英文 Gutenberg 文本拆分