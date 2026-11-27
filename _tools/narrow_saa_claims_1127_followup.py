# -*- coding: utf-8 -*-
"""SAA 收窄第二轮：补 3 处遗漏 + 修 1 处语法。字节级替换。"""
import sys
APPLY = '--apply' in sys.argv
RULES = [
    ('F01 products EN b标签遗漏',
     '<b>SAA and ETL</b> can be arranged on request for Australian and North American projects.',
     '<b>ETL</b> can be arranged on request for North American projects; <b>SAA</b> is renewed per order for Australia/New Zealand and is not currently held.',
     'products/index.html', 1),
    ('F02 bathroom 模糊 where applicable',
     'CCC for China market, and SAA/ETL where applicable.',
     'CCC for China market, ETL on request, and SAA renewal per order.',
     'bathroom-exhaust-fan-buying-guide.html', 1),
    ('F03 walkthrough 语法修正',
     'ETL documentation and SAA renewal is arranged per order;',
     'ETL documentation can be arranged on request; SAA renewal is arranged per order;',
     'baer-factory-walkthrough.html', 1),
]
fatal=[]; plan=[]
for name, old, new, path, expect in RULES:
    ob=old.encode(); nb=new.encode()
    b=open(path,'rb').read(); c=b.count(ob)
    print('%-4s %-34s %d/%d' % ('OK' if c==expect else ('DONE' if c==0 else 'FATAL'), name, c, expect))
    if c not in (0,expect): fatal.append(name)
    elif c: plan.append((path,ob,nb,name,c))
if fatal: raise SystemExit('中止：'+str(fatal))
if not any(p[4] for p in plan):
    print('\n幂等确认：3 条规则全 0，无变更。'); raise SystemExit(0)
if not APPLY:
    print('\nDRY-RUN：%d 文件 / %d 处，未落盘。' % (len(set(p[0] for p in plan)), sum(p[4] for p in plan)))
    raise SystemExit(0)
from collections import defaultdict
d=defaultdict(list)
for p,ob,nb,name,c in plan: d[p].append((ob,nb,name,c))
for p,rs in d.items():
    b=open(p,'rb').read()
    for ob,nb,name,c in rs: b=b.replace(ob,nb)
    open(p,'wb').write(b)
    print('  APPLIED',p)
