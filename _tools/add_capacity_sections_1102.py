# -*- coding: utf-8 -*-
import io, sys

P = 'baer-production-capacity.html'
s = io.open(P, encoding='utf-8', newline='').read()

ANCHOR = '<h2>Built for OEM &amp; ODM Partners</h2>'
if ANCHOR not in s:
    print('ANCHOR MISSING'); sys.exit(1)

NEW = '''  <h2>Facility at a Glance</h2>
  <p>Every figure below can be checked on a live video call or an on-site audit &mdash; we would rather you verify than take our word for it.</p>
  <table class="compare-table">
    <thead><tr><th>Item</th><th>Capacity / figure</th></tr></thead>
    <tbody>
      <tr><td>Production buildings</td><td>50,000 m&sup2; in Shengzhou, Zhejiang</td></tr>
      <tr><td>Workshops</td><td>4 production halls</td></tr>
      <tr><td>Warehouse</td><td>12,000 m&sup2; for components and finished goods</td></tr>
      <tr><td>Injection moulding</td><td>12 in-house machines for ABS / PP housings, shutters and grilles</td></tr>
      <tr><td>Motor winding</td><td>5 winding and stator stations</td></tr>
      <tr><td>Assembly lines</td><td>8 lines, one flow per product family</td></tr>
      <tr><td>In-house laboratory</td><td>Electrical parameters, dielectric strength (hi-pot), inter-turn surge, temperature rise, noise, dynamic balance</td></tr>
      <tr><td>Sample room</td><td>50 m&sup2; display room for model selection</td></tr>
      <tr><td>Annual capacity</td><td>1,000,000 units</td></tr>
      <tr><td>Annual export value</td><td>USD 3&ndash;5 million</td></tr>
      <tr><td>Export split</td><td>Middle East ~50% &middot; Europe ~30% &middot; North America ~20%</td></tr>
      <tr><td>Export sales team</td><td>5 staff &mdash; English, Chinese, Arabic</td></tr>
      <tr><td>Trade terms</td><td>EXW, FOB Ningbo / Shanghai (CIF, CFR, DDP on request)</td></tr>
    </tbody>
  </table>

  <h2>Certifications on File</h2>
  <p>Certificate numbers are published so your importer, customs broker or certification body can verify them independently before you place an order.</p>
  <table class="compare-table">
    <thead><tr><th>Certificate</th><th>Number</th><th>Issued by</th><th>Valid</th><th>Scope</th></tr></thead>
    <tbody>
      <tr><td>CE (LVD / EMC)</td><td>XH2601E0321945GC</td><td>Xihua International Testing &amp; Certification (Shenzhen) Co., Ltd.</td><td>28 Jan 2026 &ndash; 28 Jan 2031</td><td>Duct fans</td></tr>
      <tr><td>ISO 9001</td><td>04625Q15304Q1M</td><td>Beijing Head International Certification Co., Ltd.</td><td>23 Oct 2025 &ndash; 16 Nov 2028</td><td>Ventilation fan manufacture</td></tr>
      <tr><td>CCC (3C)</td><td>2024010702612682</td><td>China Quality Certification Centre (CQC)</td><td>12 Mar 2024 &ndash; 11 Mar 2029</td><td>KLT-10B, 12B, 16B, 18B &mdash; 220V 50Hz</td></tr>
      <tr><td>ETL</td><td>5024594</td><td>Intertek</td><td>19 Dec 2022 &ndash; no expiry</td><td>Ceiling mount exhaust fans, KLT-10 to KLT-30</td></tr>
      <tr><td>CB Scheme</td><td>On file &mdash; ask for the report</td><td>IEC CB scheme</td><td>&mdash;</td><td>Basis for GCC / G-Mark and national approvals</td></tr>
    </tbody>
  </table>
  <p>Need a market-specific file? SABER / SASO for Saudi Arabia, G-Mark for the GCC, SAA for Australia and ETL for North America can be arranged on request &mdash; see the <a href="/exhaust-fan-certifications-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">certification guide</a>.</p>

'''

s = s.replace(ANCHOR, NEW + ANCHOR, 1)

# 新增两条可见 FAQ（追加到 FAQ 区块末尾）
FAQ_TAIL = '<h2>Frequently Asked Questions</h2>'
if FAQ_TAIL not in s:
    print('FAQ TAIL MISSING'); sys.exit(1)

EXTRA_FAQ = '''<div class="faq-item">
  <h3>What certifications does BAER hold, and can I verify them?</h3>
  <p>CE (XH2601E0321945GC), ISO 9001 (04625Q15304Q1M), CCC (2024010702612682) and ETL (5024594), plus CB reports that convert to GCC / G-Mark. Each number is published on this page so your importer or certification body can check it independently; ask us for the PDF at any time.</p>
</div>
<div class="faq-item">
  <h3>How big is the factory and how many people work there?</h3>
  <p>50,000 m&sup2; of production buildings in Shengzhou, Zhejiang &mdash; 4 workshops, a 12,000 m&sup2; warehouse, 12 injection moulding machines, 5 winding stations and 8 assembly lines, with 50&ndash;100 staff and a 5-person export team.</p>
</div>
'''

# 插到 FAQ 最后一个 faq-item 之后之前：找到 <h2>Frequently Asked Questions</h2> 后第一个 <div class="faq-item"> 位置前插入不合适，
# 直接追加到 FAQ 区块末尾（即 </div>\n\n  <footer 之前的位置由后续段落决定）——这里改为在第一个 faq-item 前插入，保持 FAQ 顺序自然
idx = s.index(FAQ_TAIL) + len(FAQ_TAIL)
# 跳到该行结尾
nl = s.index('\n', idx) + 1
s = s[:nl] + EXTRA_FAQ + s[nl:]

# FAQ JSON-LD 同步
JSON_OLD = '"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What is BAER\'s monthly production capacity?"'
JSON_NEW = ('"@type": "FAQPage", "mainEntity": ['
            '{"@type": "Question", "name": "What certifications does BAER hold, and can I verify them?", '
            '"acceptedAnswer": {"@type": "Answer", "text": "CE (XH2601E0321945GC, valid to 2031-01-28), ISO 9001 (04625Q15304Q1M, to 2028-11-16), CCC (2024010702612682, to 2029-03-11) and ETL (5024594, no expiry), plus CB reports that convert to GCC/G-Mark. Certificate numbers are published on the factory page for independent verification."}}, '
            '{"@type": "Question", "name": "How big is the BAER factory and how many people work there?", '
            '"acceptedAnswer": {"@type": "Answer", "text": "50,000 m² of production buildings in Shengzhou, Zhejiang: 4 workshops, a 12,000 m² warehouse, 12 injection moulding machines, 5 winding stations and 8 assembly lines, with 50–100 staff and a 5-person export team."}}, '
            '{"@type": "Question", "name": "What is BAER\'s monthly production capacity?"')
if JSON_OLD not in s:
    print('JSON ANCHOR MISSING')
else:
    s = s.replace(JSON_OLD, JSON_NEW, 1)

s = s.replace('"dateModified": "2026-10-21"', '"dateModified": "2026-11-02"')
s = s.replace('Last updated: September 3, 2026', 'Last updated: November 2, 2026')

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('written', len(s))
