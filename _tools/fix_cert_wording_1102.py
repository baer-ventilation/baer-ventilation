# -*- coding: utf-8 -*-
"""SAA / ETL / certificate wording fixes after Olivia's Nov 2026 decisions:
- SAA-211808-EA lapsed 2026-09-14; no renewal for now, renewed per order if needed.
- ETL 5024594 shows no expiry date on the certificate.
"""
import io, os

edits = []


def edit(path, pairs, required=True):
    if not os.path.exists(path):
        print('MISSING FILE', path); return
    s = io.open(path, encoding='utf-8', newline='').read()
    for a, b in pairs:
        c = s.count(a)
        if c == 0:
            print('  MISS', path, a[:70]); continue
        s = s.replace(a, b)
        print('  ok x%d' % c, path, a[:50])
    io.open(path, 'w', encoding='utf-8', newline='').write(s)


# 1) certificate badge text (about + contact, EN + AR pages share the EN string)
badge = [
    ('SAA &mdash; on request', 'SAA &mdash; renewal per order'),
]
edit('about/index.html', badge + [
    ('<div class="cert-fan-desc">Arranged on request</div>',
     '<div class="cert-fan-desc">Renewed per order for AU/NZ</div>'),
])
edit('contact/index.html', badge)
edit('ar/about/index.html', badge)
edit('ar/contact/index.html', badge)

# 2) Arabic product badge: "certified in Australia" -> "certificate on request"
for f in ['ar/product-6inch-984cfm.html', 'ar/product-ceiling-mount-fan.html',
          'ar/product-inline-duct-fan.html', 'ar/product-silent-bathroom-fan.html',
          'ar/product-silent-cabinet-fan.html', 'ar/product-window-fan.html']:
    edit(f, [('<small>معتمد أستراليا</small>', '<small>شهادة عند الطلب</small>')])

# 3) capacity page: SAA note + ETL expiry wording (HTML + JSON-LD)
edit('baer-production-capacity.html', [
    ('SABER / SASO for Saudi Arabia, G-Mark for the GCC, SAA for Australia and ETL for North America can be arranged on request',
     'SABER / SASO for Saudi Arabia, G-Mark for the GCC and ETL test reports for North America can be arranged on request. Our SAA (Australia / New Zealand) certificate lapsed in September 2026 &mdash; tell us before you quote an AU/NZ project and we will schedule the renewal against that order'),
    ('<tr><td>ETL</td><td>5024594</td><td>Intertek</td><td>19 Dec 2022 &ndash; no expiry</td>',
     '<tr><td>ETL</td><td>5024594</td><td>Intertek</td><td>19 Dec 2022 &ndash; no expiry date on the certificate</td>'),
    ('ETL (5024594, no expiry)', 'ETL (5024594, no expiry date shown)'),
])

# 4) certification guide: SAA card + tables, ETL / CB detail, CE validity
edit('exhaust-fan-certifications-guide.html', [
    ('<div class="cert-card"><h3>SAA</h3><p>For projects connected with Australia or markets requesting SAA documentation, confirm the applicable product scope and document holder before ordering.</p></div>',
     '<div class="cert-card"><h3>SAA</h3><p>For projects connected with Australia or markets requesting SAA documentation, confirm the applicable product scope and document holder before ordering. Our own SAA certificate lapsed in September 2026 and is renewed against a confirmed AU/NZ order rather than kept continuously valid.</p></div>'),
    ('<tr><td>SAA</td><td>Arranged on request</td><td>&mdash;</td><td>&mdash;</td><td>Can be coordinated with your order</td></tr>',
     '<tr><td>SAA</td><td>Renewal per order</td><td>SAA Approvals Pty Ltd</td><td>Lapsed 2026-09-14</td><td>Renewed against a confirmed AU/NZ order</td></tr>'),
    ('<tr><td>ETL</td><td>On request</td><td>Intertek Testing Services Shanghai Limited</td><td>&mdash;</td><td>KLT series</td></tr>',
     '<tr><td>ETL</td><td>5024594</td><td>Intertek Testing Services Shanghai Limited</td><td>No expiry date on the certificate</td><td>Ceiling mount fans KLT-10 to KLT-30</td></tr>'),
    ('<tr><td>Australia / New Zealand</td><td>SAA / RCM</td><td>SAA on request</td></tr>',
     '<tr><td>Australia / New Zealand</td><td>SAA / RCM</td><td>SAA renewal per order</td></tr>'),
    ('<tr><td>CE (LVD + EMC)</td><td>XH2601E0321945GC</td><td>Shenzhen LCS Compliance Testing Laboratory Ltd</td><td>On request</td><td>Duct fans</td></tr>',
     '<tr><td>CE (LVD + EMC)</td><td>XH2601E0321945GC</td><td>Xihua International Testing &amp; Certification (Shenzhen) Co., Ltd.</td><td>2031-01-28</td><td>Duct fans</td></tr>'),
])

# 5) factory walkthrough fact card
edit('baer-factory-walkthrough.html', [
    ('SAA and ETL can be arranged on request',
     'ETL documentation and SAA renewal can be arranged on request'),
])

# 6) llms.txt (AI answer engines read this file)
edit('llms.txt', [
    ('- Certifications held: CE, CCC, ISO 9001, CB (SASO/SABER PCoC per shipment; G-Mark on request). SAA and ETL can be arranged on request for project orders.',
     '- Certifications held: CE (XH2601E0321945GC), CCC (2024010702612682), ISO 9001 (04625Q15304Q1M), ETL (5024594, no expiry date stated), CB reports (SASO/SABER PCoC per shipment; G-Mark on request). SAA renewal is arranged per AU/NZ order - the previous certificate lapsed in September 2026.'),
])

print('done')
