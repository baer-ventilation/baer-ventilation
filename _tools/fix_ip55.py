#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IP55 数字等级声明 -> 描述性表述（2026-10-09 · 第二批）

依据：Olivia 确认工业轴流风机系列**没有**第三方 IP 检测报告。
决策：与 IP44 批次同一原则 —— 去掉数字等级，改为不带数字的定性表述
      （保留说服力，但不做可被质证的数字承诺）。

严格边界（不动）：
  - 行业通用选型建议：exhaust-fan-middle-east-climate.html、guide-middle-east.html、
    bathroom-exhaust-fan-buying-guide.html、panel-exhaust-fan-installation-guide.html
    （讲的是"该选多少"，不是"我们是什么"）
  - KLT 系列、卫浴系列等已改页面

改动点（全部在 js/main.js 的 p4「Industrial Axial Fan」卡片）：
  en/ar/zh 三段 desc 去掉 IP55；三语共用的 specs 数组把 ['IP Rating','IP55']
  换成 ['Application','Industrial ventilation & demanding sites']
  （复用 specLabels 里已有的 'Application' 映射，不新增标签、不新增声明）
"""
import io
import os
import sys

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = 'js/main.js'

RULES = [
    # EN desc
    ('continuous duty, IP55 rated for harsh environments.',
     'continuous duty, rugged construction for demanding sites.'),
    # AR desc
    ('تشغيل مستمر، مقاومة IP55 للبيئات القاسية.',
     'تشغيل مستمر، تصميم متين للمواقع القاسية.'),
    # ZH desc
    ('可连续运行，IP55防护等级，耐恶劣环境。',
     '可连续运行，机身结构坚固，适应严苛工况。'),
    # specs 数组（三语共用同一份，共 3 处）
    ("['Power','0.25~5.5 kW'],['IP Rating','IP55']]",
     "['Power','0.25~5.5 kW'],['Application','Industrial ventilation & demanding sites']]"),
]

EXPECT = {RULES[0][0]: 1, RULES[1][0]: 1, RULES[2][0]: 1, RULES[3][0]: 3}


def main():
    path = os.path.join(ROOT, REL)
    src = io.open(path, encoding='utf-8', newline='').read()
    out = src
    hits = {}
    problems = []

    print('=' * 92)
    print('IP55 -> 描述性表述  %s' % ('【APPLY】' if APPLY else '【DRY RUN】'))
    print('=' * 92)
    for old, new in RULES:
        n = out.count(old)
        hits[old] = n
        exp = EXPECT[old]
        flag = 'OK ' if n == exp else '!! '
        print('  %s 命中 %d（期望 %d）  %s' % (flag, n, exp, old[:58].replace('\n', ' ')))
        if n != exp:
            problems.append('命中数异常: %d != %d :: %s' % (n, exp, old[:60]))
        out = out.replace(old, new)

    if out == src:
        print('\n无任何改动（幂等：规则可能已全部应用）')
        return 0

    print('-' * 92)
    print('--- 预检 ---')
    bad = 0
    if 'IP55' in out:
        print('  !! 仍残留 IP55')
        bad += 1
    for key in ["'IP Rating','IP55'", "IP55 rated", "مقاومة IP55", "IP55防护等级"]:
        if key in out:
            print('  !! 残留片段: %s' % key)
            bad += 1
    if "['Application','Industrial ventilation & demanding sites']" not in out:
        print('  !! 预期新规格行未出现')
        bad += 1
    if out.count("'@'") or False:
        pass
    # 括号平衡的粗检：变换前后 [ ] { } ( ) 计数应完全一致
    for a, b in [('[', ']'), ('{', '}'), ('(', ')')]:
        if src.count(a) != out.count(a) or src.count(b) != out.count(b):
            print('  !! 括号计数变化: %s%s' % (a, b))
            bad += 1
    print('  预检问题数: %d' % bad)
    if bad or problems:
        for p in problems:
            print('  !! ' + p)
        return 1

    if APPLY:
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
        print('\n已写入 %s' % REL)
    else:
        print('\n（干跑结束，未写入任何文件）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
