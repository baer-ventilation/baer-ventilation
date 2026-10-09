#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IP55 批次逆操作审计（2026-10-09）

手法：用 fix_ip55.py 的同一套规则，从 HEAD blob 重建 js/main.js，
      与工作区逐字节比对。一致 ⇒ 证明「除预期改动外零附带修改」。

另附：
  - 全站 IP55 残留扫描（应只剩行业建议页）
  - 全站自家声明类 IP 数字残留扫描（IP Rating / IP44 / IP55 / IPX 在各产品页）
"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = 'js/main.js'

RULES = [
    ('continuous duty, IP55 rated for harsh environments.',
     'continuous duty, rugged construction for demanding sites.'),
    ('تشغيل مستمر، مقاومة IP55 للبيئات القاسية.',
     'تشغيل مستمر، تصميم متين للمواقع القاسية.'),
    ('可连续运行，IP55防护等级，耐恶劣环境。',
     '可连续运行，机身结构坚固，适应严苛工况。'),
    ("['Power','0.25~5.5 kW'],['IP Rating','IP55']]",
     "['Power','0.25~5.5 kW'],['Application','Industrial ventilation & demanding sites']]"),
]

# 有意保留 IP 数字等级的页面（行业通用选型建议，非自家产品声明）
ALLOWED = {
    'exhaust-fan-middle-east-climate.html',
    'guide-middle-east.html',
    'bathroom-exhaust-fan-buying-guide.html',
    'panel-exhaust-fan-installation-guide.html',
}


def norm(t):
    return t.replace('\r\n', '\n')


def main():
    os.chdir(ROOT)
    bad = 0

    # ---- 1. 逆操作校验 ----
    blob = subprocess.run(['git', 'show', 'HEAD:' + REL],
                          capture_output=True).stdout.decode('utf-8')
    rebuilt = norm(blob)
    for old, new in RULES:
        rebuilt = rebuilt.replace(old, new)
    wt = norm(io.open(REL, encoding='utf-8', newline='').read())

    print('=' * 92)
    print('逆操作校验：%s' % REL)
    print('=' * 92)
    if wt == rebuilt:
        print('  OK  工作区 == HEAD blob 应用同一规则的重建结果（逐字节一致）')
    else:
        bad += 1
        a, b = wt.split('\n'), rebuilt.split('\n')
        print('  !! 不一致  行数 %d vs %d' % (len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            if x != y:
                print('     首个差异行 %d\n       工作区: %r\n       重建值: %r' % (i + 1, x[:120], y[:120]))
                break

    # ---- 2. 全站 IP55 残留 ----
    print('\n' + '=' * 92)
    print('全站 IP55 残留扫描')
    print('=' * 92)
    files = []
    for dp, dn, fn in os.walk('.'):
        dn[:] = [d for d in dn if d not in ('.git', '_tools', '.workbuddy', 'node_modules')]
        for f in fn:
            if f.endswith(('.html', '.js', '.txt', '.xml')):
                files.append(os.path.relpath(os.path.join(dp, f), '.').replace('\\', '/'))
    total = 0
    for rel in sorted(files):
        s = io.open(rel, encoding='utf-8', newline='').read()
        n = s.count('IP55')
        if not n:
            continue
        total += n
        mark = 'OK(行业建议,有意保留)' if rel in ALLOWED else '!! 未预期'
        if rel not in ALLOWED:
            bad += 1
        print('  %-52s %2d  %s' % (rel, n, mark))
    print('  IP55 合计: %d' % total)

    # ---- 3. 自家声明类 IP 数字残留 ----
    print('\n' + '=' * 92)
    print("自家声明类 IP 数字残留（'IP Rating' 规格标签 / IP44 / IPX 在非指南页）")
    print('=' * 92)
    for rel in sorted(files):
        if rel in ALLOWED:
            continue
        s = io.open(rel, encoding='utf-8', newline='').read()
        hits = []
        if "'IP Rating','" in s:
            hits.append("specs:['IP Rating',...]")
        if '<th>IP Rating</th>' in s or '<th>IP rating</th>' in s:
            hits.append('<th>IP Rating</th>')
        if 'IP44' in s:
            hits.append('IP44 x%d' % s.count('IP44'))
        if hits:
            print('  %-52s %s' % (rel, ', '.join(hits)))
            bad += 1
    print('\n  结论：以上若为空 ⇒ 站内已无「无检测报告支撑」的 IP 数字等级声明')

    print('\n' + '=' * 92)
    print('审计结果: %s' % ('全部通过 ✅' if bad == 0 else '发现 %d 处问题 ❌' % bad))
    print('=' * 92)
    return 0 if bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
