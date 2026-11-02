# -*- coding: utf-8 -*-
import io, os, re, sys

CHANGED = []

def rw(path, pairs, required=True):
    s = io.open(path, encoding='utf-8', newline='').read()
    orig = s
    miss = []
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        elif required:
            miss.append(old[:60])
    if miss:
        print('  MISS in', path, ':', miss)
    if s != orig:
        io.open(path, 'w', encoding='utf-8', newline='').write(s)
        CHANGED.append(path)
        return True
    return False

# ---------- 1) 50,000 m² 表述：占地 → 建筑面积 ----------
targets = []
for r, d, fs in os.walk('.'):
    if any(x in r for x in ['.git', 'node_modules', '_tools', 'assets']):
        continue
    for f in fs:
        if f.endswith(('.html', '.txt')):
            targets.append(os.path.join(r, f))

reps50 = [
    ('50,000 m² Zhejiang facility since 2003', '50,000 m² of production buildings in Shengzhou, Zhejiang, since 2003'),
    ('50,000 m² base in Zhejiang', '50,000 m² of production buildings in Shengzhou, Zhejiang'),
    ('50,000 m2 facility', '50,000 m² of production buildings'),
    ('50,000 m² facility', '50,000 m² of production buildings'),
]
print('== 50,000 m² 表述更正')
for p in targets:
    rw(p, reps50, required=False)

# ---------- 2) 月峰值 8 万 → 年产能 100 万台 ----------
print('== 80,000 units 更正')
cap = 'baer-production-capacity.html'
rw(cap, [
    ('8 assembly lines, 100% functional testing and 80,000 units monthly peak output',
     '8 assembly lines, 100% functional testing and an annual capacity of 1,000,000 units'),
    ('<div class="num">80,000+</div><div class="lbl">Units monthly peak output</div>',
     '<div class="num">1,000,000</div><div class="lbl">Units annual capacity</div>'),
    ('Up to 80,000 units in peak months, produced on 8 assembly lines with in-house injection molding and motor winding.',
     'Annual capacity is 1,000,000 units, produced on 8 assembly lines with in-house injection moulding and motor winding.'),
])
rw('llms.txt', [
    ('up to 80,000 units/month peak', 'annual capacity 1,000,000 units'),
    ('50,000 m² facility', '50,000 m² of production buildings in Shengzhou, Zhejiang'),
])

# ---------- 3) 100% 全铜线 → 铜/铝可选 ----------
print('== copper winding 更正')
COPPER_NEW = 'Motors are available with copper or aluminium windings — copper is recommended for continuous-duty and high-ambient installations and can be specified on any model.'
rw('faq.html', [
    ('All models use 100% copper-winding motors with ball bearings, thermal protection and continuous-duty ratings. Motor details (power, speed, shaft size, capacitor) are listed in each model&#39;s specification table.',
     COPPER_NEW + ' All models use ball bearings, thermal protection and continuous-duty ratings. Motor details (power, speed, shaft size, capacitor) are listed in each model&#39;s specification table.'),
    ('All models use <strong>100% copper-winding motors</strong> with ball bearings, thermal protection and continuous-duty ratings. Motor details (power, speed, shaft size, capacitor) are listed in each model&#39;s specification table.',
     'Motors are available with <strong>copper or aluminium windings</strong> — copper is recommended for continuous-duty and high-ambient installations and can be specified on any model. All models use ball bearings, thermal protection and continuous-duty ratings. Motor details (power, speed, shaft size, capacitor) are listed in each model&#39;s specification table.'),
])
rw('oem-private-label-exhaust-fan-guide.html', [
    ('All models use 100% copper-winding motors with ball bearings, thermal protection and continuous-duty ratings. Motor specs are listed in each model&#39;s specification table.',
     'Motors are available with copper or aluminium windings — copper is recommended for continuous-duty and high-ambient installations and can be specified on any model. All models use ball bearings, thermal protection and continuous-duty ratings. Motor specs are listed in each model&#39;s specification table.'),
    ('All models use <strong>100% copper-winding motors</strong> with ball bearings, thermal protection and continuous-duty ratings. Full motor specs are listed per model.',
     'Motors are available with <strong>copper or aluminium windings</strong> — copper is recommended for continuous-duty and high-ambient installations and can be specified on any model. All models use ball bearings, thermal protection and continuous-duty ratings. Full motor specs are listed per model.'),
])

print('changed files:', len(CHANGED))
for c in CHANGED:
    print('  ', c)
