# -*- coding: utf-8 -*-
"""侦察：/verify/ 页批次 —— 页脚底部隐私行变体 / 语言归属 / Organization 节点数 / nav 变体"""
import io, os, re, collections, json

ROOT = '.'
BOTTOM = re.compile(r'<p style="margin:14px 0 0;font-size:12px;opacity:\.85;">(.*?)</p>', re.S)
ORG = re.compile(r'"@type"\s*:\s*"Organization"')

def lang_of(p):
    p = p.lstrip('./')
    if p.startswith('ar/') or p.startswith('ar__'):
        return 'AR'
    if p.startswith('zh/') or p.startswith('zh__'):
        return 'ZH'
    return 'EN'

files = []
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dp or dp.startswith('./_tools'):
        continue
    for f in fn:
        if f.endswith('.html'):
            files.append(os.path.join(dp, f).replace('\\', '/'))
files.sort()

bottom_variants = collections.Counter()
bottom_by_lang = collections.Counter()
no_bottom = []
org_count = collections.Counter()
nav_variants = collections.Counter()
rows = []

for p in files:
    s = io.open(p, encoding='utf-8', newline='').read()
    lg = lang_of(p)
    ms = BOTTOM.findall(s)
    if ms:
        for m in ms:
            bottom_variants[m.strip()] += 1
            bottom_by_lang[(lg, m.strip()[:40])] += 1
    else:
        no_bottom.append((lg, p))
    org_count[len(ORG.findall(s))] += 1
    # nav 指纹：第一个 <nav ...> 块的 class
    nm = re.search(r'<nav[^>]*>', s)
    nav_variants[nm.group(0) if nm else 'NO_NAV'] += 1
    rows.append((lg, p, len(ms), len(ORG.findall(s))))

print("HTML 总数:", len(files))
print("\n=== 底部隐私行变体（去空白后）===")
for k, v in bottom_variants.most_common():
    print(f"[{v:3d}] {k[:160]}")
print("\n=== 无底部隐私行的文件（lang, path）===")
for lg, p in no_bottom:
    print(f"  {lg} {p}")
print("\n=== Organization 节点数分布 ===")
for k, v in sorted(org_count.items()):
    print(f"  节点数={k}: {v} 个文件")
print("\n=== nav 变体 ===")
for k, v in nav_variants.most_common():
    print(f"[{v:3d}] {k}")
