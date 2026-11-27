# -*- coding: utf-8 -*-
"""2026-11-27 SAA 口径收窄：一律 renewal per order / not currently held。
ETL 证书有效（5024594，无到期日），on request 保留。
每条规则必须精确命中预期次数，否则中止。字节级替换，不碰行尾。
"""
import glob, os, sys

APPLY = '--apply' in sys.argv

# (名称, 原文, 替换, 预期命中数)  —— 预期为 0 的规则已剔除，命中数从上一步实测
RULES = [
    # 身份句：SAA 一律不提（用户 11-27 批准"收窄成 CE/CB/CCC/ISO9001、SAA 一律不提"）
    ('E01 身份句去 SAA/ETL 括号', ' (SAA/ETL on request)', '', 1),
    ('E02 SAA+ETL can be arranged', 'SAA and ETL can be arranged on request.',
     'ETL can be arranged on request; SAA is renewed per order (not currently held).', 12),
    ('E03 SAA available AU market', 'SAA certification is available for Australia market models on request.',
     'SAA certification is renewed per order for Australia-market models; it is not currently held.', 2),
    ('E04 SAA available AU-market', 'SAA certification is available for Australia-market models on request.',
     'SAA certification is renewed per order for Australia-market models; it is not currently held.', 1),
    ('E05 FAQ SAA(AU)+ETL(NA)', 'SAA (Australia) and ETL (North America) can be arranged on request.',
     'ETL (North America) can be arranged on request; SAA (Australia) is renewed per order and not currently held.', 1),
    ('E06 FAQ strong SAA+ETL', '<strong>SAA</strong> (Australia) and <strong>ETL</strong> (North America) certifications can be arranged on request for project orders.',
     '<strong>ETL</strong> (North America) certification can be arranged on request for project orders; <strong>SAA</strong> (Australia) is renewed per order and not currently held.', 1),
    ('E07 SAA badge on request', 'SAA &mdash; on request', 'SAA &mdash; renewal per order', 4),
    ('E08 AU badge on request', 'Australia &mdash; on request', 'Australia &mdash; renewal per order', 1),
    ('E09 why-card SAA/ETL', 'SAA / ETL on request', 'ETL on request; SAA renewal per order', 1),
    ('E10 product ct SAA badge', '<div class="ct">SAA<small>On request</small></div>',
     '<div class="ct">SAA<small>Renewal per order</small></div>', 6),
    ('E11 walkthrough renewal', 'SAA renewal can be arranged on request',
     'SAA renewal is arranged per order', 1),
    ('E13 ME table scheme list', '3C / CB / SAA / ETL', '3C / CB / ETL', 1),
    # 中文
    ('C01 中文身份句去 SAA', '（SAA/ETL 可按需办理）', '', 7),
    ('C02 中文产品简介', 'SAA / ETL 可按需办理', 'ETL 可按需办理，SAA 按订单续期（当前不持证）', 7),
    ('C03 中文产品角标', '<div class="ct">SAA<small>可按需办理</small></div>',
     '<div class="ct">SAA<small>按订单续期</small></div>', 6),
    ('C04 中文认证卡', '<div class="cn">SAA 认证（可按需办理）</div>',
     '<div class="cn">SAA 认证（按订单续期）</div>', 2),
    # 阿语
    ('A01 阿语身份句去 SAA', '(SAA/ETL عند الطلب)', '', 1),
    ('A02 阿语产品简介', 'وSAA / ETL عند الطلب', 'وETL عند الطلب، أما SAA فيُجدَّد لكل طلب ولا يُحتفظ به حالياً', 7),
    ('A03 阿语产品角标', 'SAA<small>شهادة عند الطلب</small>', 'SAA<small>تجديد لكل طلب</small>', 6),
    ('A04 阿语厨房页', 'ويمكن ترتيب SAA وETL عند الطلب.',
     'ويمكن ترتيب ETL عند الطلب، أما SAA فيُجدَّد لكل طلب ولا يُحتفظ به حالياً.', 1),
    # JS 多语言字典
    ('J01 cert-saa EN', "'cert-saa': 'Australia Approved'", "'cert-saa': 'Renewal per order'", 1),
    ('J02 cert-saa AR', "'cert-saa': 'معتمد في أستراليا'", "'cert-saa': 'تجديد لكل طلب'", 1),
    ('J03 cert-saa ZH', "'cert-saa': '澳大利亚认证'", "'cert-saa': '按订单续期'", 1),
]

files = [f for f in glob.glob('**/*.html', recursive=True) + glob.glob('js/*.js')
         if '__' not in os.path.basename(f)]

# 全局预检：每条规则总命中数必须等于预期
fatal = []
plan = []  # (path, old, new, 命中数)
for name, old, new, expect in RULES:
    ob = old.encode('utf-8'); nb = new.encode('utf-8')
    total = 0
    for p in files:
        c = open(p, 'rb').read().count(ob)
        if c:
            plan.append((p, ob, nb, c, name))
            total += c
    flag = 'OK' if total == expect else ('DONE' if total == 0 else 'FATAL')
    print('%-4s %-32s %d/%d' % (flag, name, total, expect))
    if total not in (0, expect):
        fatal.append(name)

if fatal:
    print('\n中止：命中数与预期不符 ->', fatal)
    raise SystemExit(1)

if all(total == 0 for _, _, _, total in [(r[0], r[1], r[2], sum(open(p,'rb').read().count(r[1].encode()) for p in files)) for r in RULES]):
    print('\n幂等确认：23 条规则全部 0 命中，已全部应用，无变更。')
    raise SystemExit(0)

if not APPLY:
    print('\nDRY-RUN 完成：%d 条规则 / %d 文件改动 / %d 处替换，未落盘。'
          % (len(RULES), len(set(p for p, *_ in plan)), sum(x[3] for x in plan)))
    raise SystemExit(0)

# 落盘：按文件聚合，逐条替换
from collections import defaultdict
byfile = defaultdict(list)
for p, ob, nb, c, name in plan:
    byfile[p].append((ob, nb, name))

for p, rules in sorted(byfile.items()):
    b = open(p, 'rb').read()
    before = b
    for ob, nb, name in rules:
        n = b.count(ob)
        b = b.replace(ob, nb)
        print('  %-55s %-32s %d' % (p, name, n))
    if b != before:
        open(p, 'wb').write(b)

print('\nAPPLY 完成：%d 文件 / %d 处替换。' % (len(byfile), sum(x[3] for x in plan)))
