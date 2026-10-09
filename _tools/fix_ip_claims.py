#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IP44 数字等级声明 -> 描述性表述（2026-10-09）

依据：Olivia 确认「卫浴静音系列 / 6寸984cfm / BVF-150C」无第三方 IP 检测报告，
      站内唯一带 IP 等级的证书（CCC 2024010702612682）只覆盖 KLT 系列。
决策：去掉数字等级，改为不带数字的描述性表述。

严格边界（不动）：
  - 行业通用选型建议：guide-middle-east.html、exhaust-fan-middle-east-climate.html
  - IP55 声明（工业轴流风机，js/main.js）—— 不在本批范围，另行确认
  - KLT 系列产品页（本来没有 IP44 声明）
"""
import io
import json
import os
import re
import sys

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SBF_EN = ['product-silent-bathroom-fan.html']
SBF_AR = ['ar/product-silent-bathroom-fan.html', 'ar__product-silent-bathroom-fan.html']
SBF_ZH = ['zh/product-silent-bathroom-fan.html', 'zh__product-silent-bathroom-fan.html']

SIX_EN = ['product-6inch-984cfm.html']
SIX_AR = ['ar/product-6inch-984cfm.html', 'ar__product-6inch-984cfm.html']
SIX_ZH = ['zh/product-6inch-984cfm.html', 'zh__product-6inch-984cfm.html']

CMF_EN = ['product-ceiling-mount-fan.html']
CMF_AR = ['ar/product-ceiling-mount-fan.html', 'ar__product-ceiling-mount-fan.html']
CMF_ZH = ['zh/product-ceiling-mount-fan.html', 'zh__product-ceiling-mount-fan.html']

FAQ_EN_OLD = ('The IP44 rating makes it suitable for bathroom zone 2 (outside the immediate shower area). '
              'For installation directly above a shower we can advise on suitable models.')
FAQ_EN_NEW = ('The housing is sealed against normal bathroom humidity, making it suitable for standard '
              'bathroom and en-suite installations. For installation directly above a shower we can '
              'advise on suitable models.')

FAQ_AR_OLD = ('تصنيف IP44 يجعلها مناسبة لمنطقة 2 في الحمام (خارج منطقة الدش المباشرة). '
              'للتركيب فوق الدش مباشرة يمكننا تقديم النصح حول الطرزات المناسبة.')
FAQ_AR_NEW = ('الهيكل محكم ضد رطوبة الحمامات العادية، وهو مناسب للحمامات القياسية '
              'والحمامات الملحقة بالغرف. للتركيب فوق الدش مباشرة يمكننا تقديم النصح حول الطرزات المناسبة.')

FAQ_ZH_OLD = 'IP44等级适用于卫浴2区（淋浴区外圈）。淋浴正上方安装的选型建议请咨询我们。'
FAQ_ZH_NEW = '机身密封设计适配普通卫浴湿度环境。淋浴正上方安装的选型建议请咨询我们。'

GROUPS = [
    ('SBF-EN', SBF_EN, [
        ('50–220 m³/h, 26–28 dB(A), IP44, ceiling/wall/window',
         '50–220 m³/h, 26–28 dB(A), moisture-resistant housing, ceiling/wall/window'),
        ('Silent Bathroom Exhaust Fan, 26 dB IP44 | BAER Ventilation',
         'Silent Bathroom Exhaust Fan, 26 dB | BAER Ventilation'),
        ('26-28 dB quiet operation, IP44 moisture protection, CE certified',
         '26-28 dB quiet operation, moisture-resistant housing, CE certified'),
        ('Silent Bathroom Exhaust Fan — 26dB, IP44, CE | BAER Ventilation',
         'Silent Bathroom Exhaust Fan — 26dB, CE | BAER Ventilation'),
        (FAQ_EN_OLD, FAQ_EN_NEW),
        ('<tr><th>IP Rating</th><td>IP44 — moisture resistant for bathrooms</td></tr>',
         '<tr><th>Moisture Protection</th><td>Moisture-resistant housing for bathroom environments</td></tr>'),
        ('50–220 m³/h, 26–28 dB(A), IP44 moisture protection, and ceiling',
         '50–220 m³/h, 26–28 dB(A), moisture-resistant housing, and ceiling'),
        ('<h4>IP44 Moisture Proof</h4><p>Splash-resistant design compliant with bathroom safety zones.</p>',
         '<h4>Moisture-Proof Housing</h4><p>Sealed design built for humid bathroom environments.</p>'),
    ]),
    ('SBF-AR', SBF_AR, [
        ('مروحة طرد حمام صامتة — 26dB · IP44 · CE | BAER Ventilation',
         'مروحة طرد حمام صامتة — 26dB · CE | BAER Ventilation'),
        ('<h4>مقاومة الرطوبة IP44</h4><p>تصميم مقاوم للرذاذ متوافق مع مناطق أمان الحمامات.</p>',
         '<h4>هيكل مقاوم للرطوبة</h4><p>تصميم محكم للبيئات الحمامية الرطبة.</p>'),
        ('حماية من الرطوبة IP44', 'هيكل مقاوم للرطوبة'),
        ('<tr><th>درجة الحماية</th><td>IP44 — مقاومة للرطوبة للحمامات</td></tr>',
         '<tr><th>مقاومة الرطوبة</th><td>هيكل مقاوم للرطوبة للحمامات</td></tr>'),
        (FAQ_AR_OLD, FAQ_AR_NEW),
    ]),
    ('SBF-ZH', SBF_ZH, [
        ('静音卫生间排气扇 — 26dB · IP44 · CE | BAER Ventilation',
         '静音卫生间排气扇 — 26dB · CE | BAER Ventilation'),
        ('<tr><th>防护等级</th><td>IP44 — 卫浴防潮</td></tr>',
         '<tr><th>防潮性能</th><td>防潮机身，适配卫浴环境</td></tr>'),
        ('<h4>IP44防潮</h4><p>防溅水设计，符合卫浴安全分区要求。</p>',
         '<h4>防潮机身</h4><p>密封设计，适配潮湿卫浴环境。</p>'),
        ('IP44防潮防护', '防潮机身'),
        (FAQ_ZH_OLD, FAQ_ZH_NEW),
    ]),
    ('SIX-EN', SIX_EN, [
        ('<tr><th>Protection</th><td>IP44 — dust & splash resistant</td></tr>',
         '<tr><th>Protection</th><td>Moisture-resistant housing</td></tr>'),
    ]),
    ('SIX-AR', SIX_AR, [
        ('<tr><th>درجة الحماية</th><td>IP44 — مقاومة للغبار والرذاذ</td></tr>',
         '<tr><th>درجة الحماية</th><td>هيكل مقاوم للرطوبة</td></tr>'),
    ]),
    ('SIX-ZH', SIX_ZH, [
        ('<tr><th>防护等级</th><td>IP44 — 防尘防溅水</td></tr>',
         '<tr><th>防护等级</th><td>防潮机身</td></tr>'),
    ]),
    ('CMF-EN', CMF_EN, [
        ('For direct shower-zone installations we recommend the IP44-rated bathroom series.',
         'For direct shower-zone installations we recommend our bathroom series.'),
    ]),
    ('CMF-AR', CMF_AR, [
        ('للتركيب المباشر في منطقة الاستحمام ننصح بسلسلة الحمامات بتصنيف IP44.',
         'للتركيب المباشر في منطقة الاستحمام ننصح بسلسلة الحمامات لدينا.'),
    ]),
    ('CMF-ZH', CMF_ZH, [
        ('淋浴正上方安装建议选用IP44防护等级的卫浴系列。',
         '淋浴正上方安装建议选用我们的卫浴系列。'),
    ]),
    ('CVW', ['ceiling-vs-window-fan.html'], [
        ('<tr><td>IP rating available</td><td>IP44–IP55</td><td>IP44</td></tr>',
         '<tr><td>Moisture protection</td><td>Moisture-resistant housing</td><td>Moisture-resistant housing</td></tr>'),
        ('<tr><td>BVF-150C</td><td>Ceiling</td><td>180 m³/h</td><td>Ultra-quiet 28dB, IP44</td></tr>',
         '<tr><td>BVF-150C</td><td>Ceiling</td><td>180 m³/h</td><td>Ultra-quiet 28 dB(A), moisture-resistant</td></tr>'),
    ]),
    ('SAUDI-EN', ['saudi-arabia-exhaust-fan-supplier.html'], [
        ('26&nbsp;dB, IP44, designed for en-suites', '26&nbsp;dB, designed for en-suites'),
    ]),
    ('SAUDI-AR', ['ar/saudi-arabia-exhaust-fan-supplier.html'], [
        ('26 ديسيبل، حماية IP44، مصممة', '26 ديسيبل، مصممة'),
    ]),
    ('LLMS', ['llms.txt'], [
        ('26 dB, IP44 bathroom fan.', '26 dB moisture-resistant bathroom fan.'),
    ]),
    ('MAINJS', ['js/main.js'], [
        ('specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'IP Rating\',\'IP44 (bathroom safe)\']',
         'specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'Moisture Protection\',\'Moisture-resistant housing\']'),
        ('specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'IP Rating\',\'IP44 (مقاوم للرطوبة)\']',
         'specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'Moisture Protection\',\'هيكل مقاوم للرطوبة\']'),
        ('specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'IP Rating\',\'IP44（浴室安全）\']',
         'specs: [[\'Airflow\',\'50~220 m³/h\'],[\'Noise\',\'≤28 dB(A)\'],[\'Moisture Protection\',\'防潮机身\']'),
        ("    'IP Rating':       ['IP Rating',       'IP',               'IP防护等级','IP'],",
         "    'IP Rating':       ['IP Rating',       'IP',               'IP防护等级','IP'],\n\n"
         "    'Moisture Protection': ['Moisture Protection','الحماية من الرطوبة','防潮性能',''],"),
    ]),
]


def ld_blocks(text):
    return re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)


def main():
    changed = {}
    problems = []
    print('=' * 96)
    print('IP44 -> 描述性表述  %s' % ('【APPLY】' if APPLY else '【DRY RUN】'))
    print('=' * 96)
    for tag, files, rules in GROUPS:
        for rel in files:
            path = os.path.join(ROOT, rel)
            if not os.path.exists(path):
                problems.append('MISSING FILE: %s' % rel)
                continue
            src = io.open(path, encoding='utf-8', newline='').read()
            out = src
            hits = []
            for old, new in rules:
                n = out.count(old)
                hits.append(n)
                if n == 0:
                    problems.append('NO MATCH [%s] %s :: %s' % (tag, rel, old[:60].replace('\n', ' ')))
                else:
                    out = out.replace(old, new)
            if out != src:
                changed[rel] = (src, out, sum(hits))
                print('  [%s] %-52s 命中 %s' % (tag, rel, hits))
    print('-' * 96)
    print('待写入文件数: %d' % len(changed))
    if problems:
        print('\n!! 问题 %d 条:' % len(problems))
        for p in problems:
            print('   ' + p)
        return 1

    print('\n--- 预检 ---')
    bad = 0
    for rel, (src, out, cnt) in sorted(changed.items()):
        if 'IP44' in out:
            print('  !! %s 仍残留 IP44: %s' % (rel, re.findall(r'.{0,40}IP44.{0,40}', out)))
            bad += 1
        if rel.endswith('.html'):
            for i, blk in enumerate(ld_blocks(out)):
                try:
                    json.loads(blk)
                except Exception as e:
                    print('  !! %s JSON-LD block#%d 解析失败: %s' % (rel, i, e))
                    bad += 1
    print('  预检问题数: %d' % bad)
    if bad:
        return 1

    if APPLY:
        for rel, (src, out, cnt) in changed.items():
            io.open(os.path.join(ROOT, rel), 'w', encoding='utf-8', newline='').write(out)
        print('\n已写入 %d 个文件' % len(changed))
    else:
        print('\n（干跑结束，未写入任何文件）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
