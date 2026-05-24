#!/usr/bin/env python3
"""将中文数字文件名批量改为阿拉伯数字。"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 完整的中文数字→阿拉伯数字映射
CN_MAP = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
}

def cn_to_num(s):
    """将中文数字字符串正确转为阿拉伯数字（支持1-99）"""
    if s == '序':
        return 0
    if s in CN_MAP:
        return CN_MAP[s]
    
    # 复合: 二十五 → 25, 五十七 → 57
    # 格式: [一到九]?十[一到九]?
    if '百' in s or '千' in s:
        return None  # 不支持百位以上
    
    result = 0
    if s.startswith('十'):
        result = 10
        s = s[1:]
    elif len(s) >= 2 and s[1] == '十':
        result = CN_MAP.get(s[0], 0) * 10
        s = s[2:]
    
    for ch in s:
        if ch in CN_MAP:
            result += CN_MAP[ch]
    
    return result

def rename_files(directory):
    """重命名目录下所有中文数字开头的文件"""
    full_dir = os.path.join(BASE, directory)
    if not os.path.isdir(full_dir):
        print(f'  ⚠️  {directory} 不存在')
        return

    renames = []
    for f in os.listdir(full_dir):
        if f.startswith('.') or f == 'MANIFEST.md' or f == 'salt-seven-friend-cn.md':
            continue

        # 匹配: 中文数字[-.]xxx.md
        m = re.match(r'^([\u4e00-\u9fff]+)([-.][^.]+\.md)$', f)
        if m:
            cn = m.group(1)
            num = cn_to_num(cn)
            if num is not None:
                newname = f'{num:02d}{m.group(2)}'
                renames.append((f, newname))

    if not renames:
        print(f'  ℹ️  {directory} 无中文数字文件名')
        return

    for old, new in renames:
        oldpath = os.path.join(full_dir, old)
        newpath = os.path.join(full_dir, new)
        os.rename(oldpath, newpath)
        print(f'  ✅ {old} → {new}')

    print(f'  📁 {directory}: {len(renames)} 个文件已重命名')

# 处理目录
dirs = [
    'library/biography/salt-seven',
    'library/biography/alexander-lee',
]
for i in [1, 2, 3]:
    d = f'library/machiavelli/discourses/book{i}'
    if os.path.isdir(os.path.join(BASE, d)):
        dirs.append(d)

for d in dirs:
    rename_files(d)
    print()

print('✅ P0.2 完成')
