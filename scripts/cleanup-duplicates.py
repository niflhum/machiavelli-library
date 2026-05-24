#!/usr/bin/env python3
"""P0.3 清理重复文件：full 文件 + '2' 后缀重复 + 纯数字名重复"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. 删除 7 个 *-full.md 文件
full_files = [
    'library/machiavelli/prince/prince-cn-full.md',
    'library/machiavelli/prince/en/prince-en-full.md',
    'library/machiavelli/art-of-war/art-of-war-cn-full.md',
    'library/machiavelli/art-of-war/art-of-war-full.md',
    'library/machiavelli/florentine/florentine-cn-full.md',
    'library/machiavelli/diplomatic/upper/diplomatic-upper-full.md',
    'library/machiavelli/diplomatic/lower/diplomatic-lower-full.md',
]

print('=== 清理 *-full.md ===')
for f in full_files:
    fp = os.path.join(BASE, f)
    if os.path.exists(fp):
        os.remove(fp)
        print(f'  ✅ 已删除 {f}')
    else:
        print(f'  ⚠️ 不存在 {f}')

# 2. 删除 discourses book2/3 中的 " 2" 后缀重复文件
print('\n=== 清理 "2" 后缀重复 ===')
for book in ['book2', 'book3']:
    d = os.path.join(BASE, f'library/machiavelli/discourses/{book}')
    if not os.path.isdir(d):
        continue
    count = 0
    for f in os.listdir(d):
        if ' 2.md' in f or ' 2.' in f:
            fp = os.path.join(d, f)
            os.remove(fp)
            count += 1
            print(f'  ✅ 已删除 {book}/{f}')
    if count == 0:
        print(f'  ℹ️  {book} 无 "2" 后缀文件')

# 3. 删除 salt-seven 中纯中文数字名文件（保留 -第X章.md 版本）
print('\n=== 清理 salt-seven 纯数字名重复 ===')
salt_dir = os.path.join(BASE, 'library/biography/salt-seven')
count = 0
for f in os.listdir(salt_dir):
    # 纯中文数字开头的 .md（如 一.md, 序.md）
    if re.match(r'^[\u4e00-\u9fff]+\.md$', f):
        fp = os.path.join(salt_dir, f)
        os.remove(fp)
        count += 1
        print(f'  ✅ 已删除 salt-seven/{f}')

# 同样清理 alexander-lee
alex_dir = os.path.join(BASE, 'library/biography/alexander-lee')
count2 = 0
if os.path.isdir(alex_dir):
    for f in os.listdir(alex_dir):
        if re.match(r'^[\u4e00-\u9fff]+\.md$', f):
            fp = os.path.join(alex_dir, f)
            os.remove(fp)
            count2 += 1
            print(f'  ✅ 已删除 alexander-lee/{f}')

# 清理 discourses book1-3 中纯中文数字名文件
for book in ['book1', 'book2', 'book3']:
    d = os.path.join(BASE, f'library/machiavelli/discourses/{book}')
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        if re.match(r'^[\u4e00-\u9fff]+\.md$', f):
            fp = os.path.join(d, f)
            os.remove(fp)
            count += 1
            print(f'  ✅ 已删除 discourses/{book}/{f}')

print(f'\n✅ P0.3 完成: 共清理 {len(full_files) + count + count2} 个重复文件')
