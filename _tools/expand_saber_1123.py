#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Expand SABER/SASO guide: 6 tables, 10 photos + 3 schematic SVGs, ~2700 words.
Byte-level edit, preserves CRLF. Dry-run by default; pass --apply to write."""
import sys, re

PATH = "saber-saso-exhaust-fan-certification.html"
APPLY = "--apply" in sys.argv

with open(PATH, "rb") as f:
    raw = f.read()
assert raw.count(b"\r\n") > 300 and raw.count(b"\n") == raw.count(b"\r\n"), "expected CRLF file"

NL = "\r\n"
def crlf(s):
    return s.replace("\n", NL)

# Each entry: (anchor, insertion to place BEFORE anchor, label)
def fig(src, alt, cap, w=960, h=720):
    return (f'<figure style="margin:26px 0;text-align:center;">' + "\n"
            f'  <img src="/images/{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">' + "\n"
            f'  <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">{cap}</figcaption>' + "\n"
            f'</figure>' + "\n")

SVG_FLOW = '''<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px;margin:24px 0;text-align:center;">
<svg viewBox="0 0 920 210" width="100%" style="max-width:860px;height:auto;" role="img" aria-label="Schematic: Saudi fan certification sequence from G-Mark to customs clearance">
  <defs><marker id="ar1" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#64748B"/></marker></defs>
  <g font-family="Arial,sans-serif" font-size="13" text-anchor="middle">
    <g><rect x="10" y="30" width="130" height="60" rx="8" fill="#fff" stroke="#0f1f3d" stroke-width="1.5"/><text x="75" y="54" fill="#0f1f3d" font-weight="700">G-Mark</text><text x="75" y="74" fill="#475569" font-size="11">GCC certificate</text></g>
    <g><rect x="165" y="30" width="130" height="60" rx="8" fill="#fff" stroke="#0f1f3d" stroke-width="1.5"/><text x="230" y="54" fill="#0f1f3d" font-weight="700">Classify</text><text x="230" y="74" fill="#475569" font-size="11">12-digit HS code</text></g>
    <g><rect x="320" y="30" width="130" height="60" rx="8" fill="#fff" stroke="#0f1f3d" stroke-width="1.5"/><text x="385" y="54" fill="#0f1f3d" font-weight="700">CAB review</text><text x="385" y="74" fill="#475569" font-size="11">technical file</text></g>
    <g><rect x="475" y="30" width="130" height="60" rx="8" fill="#FEF2F2" stroke="#C0392B" stroke-width="1.5"/><text x="540" y="54" fill="#C0392B" font-weight="700">PCoC</text><text x="540" y="74" fill="#475569" font-size="11">product, 1 year</text></g>
    <g><rect x="630" y="30" width="130" height="60" rx="8" fill="#FEF2F2" stroke="#C0392B" stroke-width="1.5"/><text x="695" y="54" fill="#C0392B" font-weight="700">SCoC</text><text x="695" y="74" fill="#475569" font-size="11">per shipment</text></g>
    <g><rect x="785" y="30" width="125" height="60" rx="8" fill="#fff" stroke="#0f1f3d" stroke-width="1.5"/><text x="847" y="54" fill="#0f1f3d" font-weight="700">FASAH</text><text x="847" y="74" fill="#475569" font-size="11">customs release</text></g>
    <g stroke="#64748B" stroke-width="1.6" marker-end="url(#ar1)">
      <line x1="140" y1="60" x2="163" y2="60"/><line x1="295" y1="60" x2="318" y2="60"/><line x1="450" y1="60" x2="473" y2="60"/><line x1="605" y1="60" x2="628" y2="60"/><line x1="760" y1="60" x2="783" y2="60"/>
    </g>
    <text x="460" y="140" fill="#475569" font-size="12">The importer holds the SABER account; PCoC and SCoC are tied to its commercial registration.</text>
    <text x="460" y="166" fill="#475569" font-size="12">The manufacturer supplies the technical file (CB report, G-Mark, EMC, label artwork, ISO 9001).</text>
  </g>
</svg>
<p style="font-size:11.5px;color:#94A3B8;margin:10px 0 0;">Schematic only — a simplified sequence for orientation, not an official SASO/SABER diagram. Always confirm the current route for your exact HS code.</p>
</div>
'''

SVG_TIMELINE = '''<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px;margin:24px 0;text-align:center;">
<svg viewBox="0 0 900 250" width="100%" style="max-width:840px;height:auto;" role="img" aria-label="Schematic: validity periods of G-Mark, PCoC, CB report and SCoC">
  <g font-family="Arial,sans-serif" font-size="13">
    <line x1="150" y1="55" x2="860" y2="55" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="150" y1="115" x2="860" y2="115" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="150" y1="175" x2="860" y2="175" stroke="#CBD5E1" stroke-width="2"/>
    <line x1="150" y1="235" x2="860" y2="235" stroke="#CBD5E1" stroke-width="2"/>
    <text x="10" y="60" fill="#0f1f3d" font-weight="700">PCoC</text>
    <text x="10" y="120" fill="#0f1f3d" font-weight="700">G-Mark</text>
    <text x="10" y="180" fill="#0f1f3d" font-weight="700">SCoC</text>
    <text x="10" y="240" fill="#0f1f3d" font-weight="700">CB report</text>
    <rect x="150" y="44" width="300" height="22" rx="6" fill="#C0392B"/><text x="300" y="60" fill="#fff" font-size="11">12 months — renew annually</text>
    <rect x="450" y="44" width="300" height="22" rx="6" fill="#F5B7B1"/><text x="600" y="60" fill="#78350F" font-size="11">renew before expiry</text>
    <rect x="150" y="104" width="520" height="22" rx="6" fill="#0f1f3d"/><text x="410" y="120" fill="#fff" font-size="11">3 years (typical)</text>
    <rect x="150" y="164" width="90" height="22" rx="6" fill="#C0392B"/><rect x="270" y="164" width="90" height="22" rx="6" fill="#C0392B"/><rect x="390" y="164" width="90" height="22" rx="6" fill="#C0392B"/>
    <text x="500" y="180" fill="#475569" font-size="11">one bar = one shipment; a new SCoC every time</text>
    <rect x="150" y="224" width="360" height="22" rx="6" fill="#64748B"/><text x="330" y="240" fill="#fff" font-size="11">valid only within its report window</text>
    <text x="540" y="240" fill="#475569" font-size="11">check the date before shipment</text>
  </g>
</svg>
<p style="font-size:11.5px;color:#94A3B8;margin:10px 0 0;">Schematic only — bars show relative validity, not a calendar or official timeline. Confirm exact periods on your own certificates.</p>
</div>
'''

SVG_HS = '''<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px;margin:22px 0;text-align:center;">
<svg viewBox="0 0 720 190" width="100%" style="max-width:660px;height:auto;" role="img" aria-label="Schematic: how the HS code 8414512000 breaks into sections">
  <g font-family="Arial,sans-serif" text-anchor="middle">
    <rect x="30" y="45" width="150" height="70" rx="8" fill="#0f1f3d"/><text x="105" y="76" fill="#fff" font-size="26" font-weight="800">8414</text><text x="105" y="100" fill="#CBD5E1" font-size="11">fans &amp; blowers</text>
    <rect x="195" y="45" width="150" height="70" rx="8" fill="#C0392B"/><text x="270" y="76" fill="#fff" font-size="26" font-weight="800">51</text><text x="270" y="100" fill="#fff" font-size="11">≤125 W self-contained</text>
    <rect x="360" y="45" width="150" height="70" rx="8" fill="#334155"/><text x="435" y="76" fill="#fff" font-size="24" font-weight="800">20</text><text x="435" y="100" fill="#CBD5E1" font-size="11">national subheading</text>
    <rect x="525" y="45" width="150" height="70" rx="8" fill="#64748B"/><text x="600" y="76" fill="#fff" font-size="24" font-weight="800">00</text><text x="600" y="100" fill="#fff" font-size="11">further digits</text>
    <text x="360" y="155" fill="#475569" font-size="12.5">China export code 8414512000 — Saudi uses a 12-digit national code; confirm the full number with your importer.</text>
  </g>
</svg>
<p style="font-size:11.5px;color:#94A3B8;margin:10px 0 0;">Schematic only — digit grouping is illustrative. Classification must be confirmed against the current tariff in force.</p>
</div>
'''

# --- New section: SASO 2663/2874 are air-conditioner standards, not fan standards ---
AC_SCOPE = '''  <h2>SASO 2663 and 2874 Are Air-Conditioner Rules — Not Fan Rules</h2>
  <p>A frequent source of confusion in 2026 comes from the updated Saudi energy-efficiency standards. <strong>SASO 2663:2025 and SASO 2874:2025</strong> govern the SEER (Seasonal Energy Efficiency Ratio) rating of <em>air conditioners</em> — window and single-split units up to 65,000 Btu/h under 2663, and large commercial systems (VRF, chillers, computer-room units) above that threshold under 2874. Both take effect on 1 December 2026.</p>
  <p><strong>Neither standard applies to ventilating or exhaust fans.</strong> A fan moves air; it has no refrigeration circuit and no SEER rating. When a supplier quotes an "SASO 2663 certificate" for a wall or inline fan, either the standard has been misidentified or the product has been misdeclared. For fans, the relevant safety basis remains IEC 60335-1 with IEC 60335-2-80, evidenced by a CB report and the SABER route described above.</p>
  <div class="note">
    <p><strong>Why this matters commercially:</strong> if an importer files a fan under an air-conditioner regulation, the application can stall or be rejected for a standard that simply does not fit the product. Ask your CAB to confirm the applicable technical regulation in writing against your exact HS code before paying for tests you do not need.</p>
  </div>
  <p>We separately explain the fan-specific standards — CE, CB, ISO and what each certificate actually proves — in our <a href="/exhaust-fan-certifications-guide" style="color:#C0392B;font-weight:700;">exhaust fan certifications guide</a>.</p>
'''

# --- Table 5: validity & renewal ---
VALIDITY = '''  <h2>Certificate Validity and Renewal at a Glance</h2>
  <p>Renewals fail far more often than first applications. This table gives the working periods importers plan around so a certificate does not quietly expire mid-order.</p>
  <table class="compare-table">
    <thead><tr><th>Item</th><th>Typical validity</th><th>Who acts</th><th>Renewal trigger</th></tr></thead>
    <tbody>
      <tr><td>G-Mark (GCC)</td><td>3 years (typical)</td><td>Manufacturer</td><td>Before expiry; model must stay identical</td></tr>
      <tr><td>PCoC</td><td>12 months</td><td>Saudi importer</td><td>Annual — renew before the next shipment</td></tr>
      <tr><td>SCoC</td><td>One consignment</td><td>Saudi importer</td><td>Every shipment; cannot be backdated</td></tr>
      <tr><td>CB test report</td><td>Within its report window</td><td>Manufacturer</td><td>Re-test or reissue when the report dates out</td></tr>
      <tr><td>ISO 9001 factory certificate</td><td>3 years (typical, with audits)</td><td>Manufacturer</td><td>Surveillance audits keep it current</td></tr>
    </tbody>
  </table>
'''

# --- Table 6: timeline (SASO published service periods) ---
TIMELINE = '''  <h2>Realistic Timeline for a First Shipment</h2>
  <p>Timing splits into two stages. SASO publishes indicative service periods — around <strong>8 working days</strong> for product-conformity registration and <strong>3 working days</strong> for an imported commercial shipment certificate — but actual elapsed time depends on document readiness and whether a CAB asks for extra testing or a factory audit. Budget for the whole chain, not just the portal step.</p>
  <table class="compare-table">
    <thead><tr><th>Stage</th><th>Main action</th><th>Who drives it</th><th>Indicative time</th></tr></thead>
    <tbody>
      <tr><td>Classification</td><td>Confirm 12-digit HS code and applicable regulation</td><td>Importer / CAB</td><td>1–2 working days</td></tr>
      <tr><td>File review</td><td>Check CB report, G-Mark, EMC, label artwork</td><td>Manufacturer + CAB</td><td>Varies with file quality</td></tr>
      <tr><td>PCoC registration</td><td>Product certificate issued on SABER</td><td>CAB / SASO</td><td>~8 working days (SASO service target)</td></tr>
      <tr><td>Production + documents</td><td>Build the order; prepare invoice, packing list, B/L</td><td>Manufacturer / exporter</td><td>Overlaps with PCoC</td></tr>
      <tr><td>SCoC issuance</td><td>Shipment certificate before arrival</td><td>Importer / CAB</td><td>~3 working days once data is final</td></tr>
    </tbody>
  </table>
  <p>The practical rule: start the file at PO confirmation so the PCoC is issued while the goods are still in production. A complete first submission is the single biggest lever on elapsed time.</p>
'''

# --- edits: (anchor, insertion, label) ---
edits = []
edits.append(('  <h2>SASO, SALEEM and SABER: What Each One Does</h2>', SVG_FLOW, 'svg-flow'))
edits.append(('  <h2>PCoC vs SCoC: The Two Certificates</h2>',
              fig('baer-certificate-wall', 'BAER certificate wall with product and factory certificates',
                  'A certificate wall is a starting point, not proof — each certificate must be checked against the model and the current date.', 960, 640),
              'photo-certwall'))
edits.append(('  <h2>The Process, Step by Step</h2>', VALIDITY + SVG_TIMELINE, 'validity-table+svg'))
edits.append(('  <h2>HS Codes for Exhaust Fans</h2>', SVG_HS, 'svg-hs'))
edits.append(('  <h2>Technical Standards and Test Reports</h2>',
              fig('baer-hi-pot-test', 'Hi-pot (dielectric withstand) test on a production fan',
                  'Safety tests such as dielectric withstand feed the CB report used in a SABER file.', 960, 640),
              'photo-hipot'))
edits.append(('  <h2>Document Checklist</h2>',
              fig('motor-test-bench', 'Fan motor being checked on a test bench',
                  'Motor and performance checks generate the test data a CAB reviews.', 960, 640),
              'photo-motortest'))
edits.append(('  <h2>Arabic Labelling and Marking</h2>', TIMELINE, 'timeline-table'))
edits.append(('  <h2>Sequencing Certification with Your Order</h2>',
              fig('baer-export-cartons-warehouse', 'Export cartons staged in the BAER warehouse',
                  'Carton marking is checked against the SABER record; artwork should be fixed before mass production.', 960, 640),
              'photo-cartons'))
edits.append(('  <h2>Why Applications Get Rejected</h2>',
              fig('baer-factory-sign-legal-name', 'BAER factory sign showing the registered company name',
                  'Factory identity on documents must match the legal entity on the business licence.', 960, 640),
              'photo-factorysign'))
edits.append(('  <h2>What BAER Supplies</h2>', AC_SCOPE, 'ac-scope-section'))
edits.append(('  <h2>Frequently Asked Questions</h2>',
              fig('panel-fan-assembly-line', 'Panel exhaust fans on the BAER assembly line',
                  'Model-specific specification sheets let an importer register each variant accurately.', 960, 640),
              'photo-assembly'))
edits.append(('  <h2>What BAER Supplies</h2>',
              fig('baer-sample-room', 'BAER sample room with fan models on display',
                  'Samples and drawings are prepared per model so the technical file matches what ships.', 960, 640),
              'photo-samples'))
edits.append(('  <div class="cta-box">',
              fig('winding-station', 'Motor winding station at the BAER factory',
                  'Factory process documentation supports the ISO 9001 part of the submission.', 960, 640),
              'photo-winding'))

text = raw.decode('utf-8')
new = 0
for anchor, ins, label in edits:
    cnt = text.count(anchor)
    ins_crlf = crlf(ins)
    marker = '<!-- EXPANDED:' + label + ' -->'
    if marker in text:
        print('SKIP', label, '(already applied)')
        continue
    if cnt != 1:
        print('FAIL anchor count', cnt, 'for', label, '::', anchor[:60])
        sys.exit(1)
    block = marker + NL + ins_crlf + anchor
    if APPLY:
        text = text.replace(anchor, block, 1)
    new += 1
    print('NEW ', label, '-> inserted before:', anchor[:55])

print('TOTAL NEW EDITS:', new)

# date fields are pure replacements (not insertions)
for old, newv, label in [
    ('Last updated: November 18, 2026', 'Last updated: November 23, 2026', 'date-visible'),
    ('"dateModified": "2026-11-18"', '"dateModified": "2026-11-23"', 'date-jsonld'),
]:
    c = text.count(old)
    if newv in text and old not in text:
        print('SKIP', label, '(already applied)')
    elif c == 1:
        if APPLY:
            text = text.replace(old, newv, 1)
        print('NEW ', label, '-> replaced')
    else:
        print('FAIL date', label, 'count', c)
        sys.exit(1)

if not APPLY:
    print('DRY RUN only. Pass --apply to write.')
    sys.exit(0)

out = text.encode('utf-8')
assert out.count(b'\r\n') > 0 and out.count(b'\n') == out.count(b'\r\n'), 'CRLF broken after write!'
with open(PATH, 'wb') as f:
    f.write(out)
print('WRITTEN', PATH, 'bytes', len(out))
