---
name: machiavelli-library
name-en: Machiavelli Library
description: 马基雅维利原文图书馆（中英双语）——用原文回答关于马基雅维利的一切问题。
description-en: A bilingual (Chinese-English) searchable library of Machiavelli's original texts. Ask any question and receive verbatim passages with citations in both languages.
category: research
tags: [machiavelli, philosophy, history, italian-renaissance, florence, political-theory]
version: "1.0.0"
author: built from public domain sources and user-provided texts
triggers:
  prefix:
    - /machlib
    - machiavelli-library
    - 马基雅维利图书馆
  keyword:
    - machiavelli原文
    - machiavelli quote
    - 马基雅维利说过
    - 马基雅维利在哪
    - 马基雅维利原文
---

## 这是什么

马基雅维利图书馆是一个**可检索的原文库**（中英双语）。它不是对话分身，不给你建议，不分析你的处境。它只做一件事：**找到马基雅维利在某处说过的原文，把原文给你看。**

## 收录内容

| 类别 | 著作 | 语言 | 格式 |
|------|------|------|------|
| 马基雅维利著作 | 《君主论》 | 中英 | 按章分文件 |
| 马基雅维利著作 | 《论李维》 | 中英 | 按卷/章分文件 |
| 马基雅维利著作 | 《佛罗伦萨史》 | 中英 | 按卷分文件 |
| 马基雅维利著作 | 《兵法》 | 英文 | 按卷分文件 |
| 马基雅维利著作 | 书信集（上下） | 中文 | 按年份 |
| 马基雅维利著作 | 政务与外交著作（上下） | 中文 | 按篇目 |
| 传记 | 《我的朋友马基雅维利》盐野七生 | 中文 | 按章分文件 |
| 传记 | 《马基雅维利：他的生活与时代》亚历山大·李 | 中文 | 按部分文件 |
| 研究 | 《马基雅维利语录》盐野七生 | 中文 | 按篇分文件 |
| 研究 | 《解读马基雅维利》麦考米克 | 中文 | 按章分文件 |
| 小说 | 《彼时此时——马基雅维利在伊莫拉》毛姆 | 中文 | 按章分文件 |

## 使用方式

你可以说：
- "马基雅维利怎么看待机运？给我原文"
- "马基雅维利说过什么关于守信的话？原文是什么"
- "《君主论》第 18 章的完整内容是什么"
- "马基雅维利书信 224 写了什么"
- "马基雅维利骂过美第奇吗？给我原文"
- "What does Machiavelli say about fortune in The Prince?"

## 检索规则

1. 理解用户的问题，提取关键词（中英文均可）
2. 先在 `index/themes.md` 中查找预建索引
3. 如果索引没有，搜索 `library/` 目录下所有文件
4. 返回最相关的 3-5 个原文段落
5. 每个结果必须标注：著作名 + 章节/书信编号 + 原文
6. 只返回原文，不加分析，不加人格，不加语气

## 重要限制

- **只返回原文**，不分析，不建议，不联想
- 如果找不到相关内容，直接说"图书馆中没有找到相关内容"
- 不编造原文，查不到就说查不到
- 书信集只收录有公版来源的信件，不确定时标注「此信无公版来源」