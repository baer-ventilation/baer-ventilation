#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逆操作审计：用 fix_ip_claims.py 的同一套规则从 HEAD blob 重建目标文件，
与工作区逐字节比对。0 差异 => 证明除预期替换外零附带修改。"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_ip_claims as F  # noqa: E402

ROOT = F.ROOT
norm = lambda t: t.replace('\r\n', '\n')

ok = bad = 0
bad_list = []
for tag, files, rules in F.GROUPS:
    for rel in files:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            bad += 1
            bad_list.append(rel + ' (missing)')
            continue
        wt = io.open(path, encoding='utf-8', newline='').read()
        blob = subprocess.run(['git', 'show', 'HEAD:' + rel], cwd=ROOT,
                              capture_output=True).stdout.decode('utf-8')
        rebuilt = norm(blob)
        for old, new in rules:
            rebuilt = rebuilt.replace(old, new)
        if norm(wt) == rebuilt:
            ok += 1
        else:
            bad += 1
            bad_list.append(rel)
            a = norm(wt).split('\n')
            b = rebuilt.split('\n')
            for i, (x, y) in enumerate(zip(a, b)):
                if x != y:
                    print('  首个差异 %s 行%d:\n    工作区=%r\n    重建  =%r' % (rel, i, x[:110], y[:110]))
                    break
            else:
                print('  行数差异 %s: 工作区=%d 重建=%d' % (rel, len(a), len(b)))

print('=' * 80)
print('逆操作审计: OK=%d  BAD=%d  (共 %d 文件)' % (ok, bad, ok + bad))
if bad_list:
    print('异常文件:')
    for x in bad_list:
        print('  ' + x)
print('=' * 80)

print('\n--- 全站 IP44 残留扫描（应只剩行业通用建议页）---')
os.chdir(ROOT)
out = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split()
hit = {}
for rel in out:
    if not os.path.exists(rel) or os.path.isdir(rel):
        continue
    try:
        s = io.open(rel, encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    if 'IP44' in s:
        hit[rel] = s.count('IP44')
for k, v in sorted(hit.items()):
    print('  %-58s %d' % (k, v))
print('  （命中文件数 %d）' % len(hit))
print('\n--- IP55 残留（本批未处理，应保持原样）---')
for rel in out:
    if not os.path.exists(rel) or os.path.isdir(rel):
        continue
    try:
        s = io.open(rel, encoding='utf-8', errors='ignore').read()
    except Exception:
        continue
    if 'IP55' in s:
        print('  %-58s %d' % (rel, s.count('IP55')))
