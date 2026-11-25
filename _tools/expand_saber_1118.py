# -*- coding: utf-8 -*-
"""Expand SABER page 2026-11-18: Arabic labelling section, order-sequencing section, 3 new FAQs, RFQ + ar links, dates."""
import json, sys

P = "saber-saso-exhaust-fan-certification.html"
b = open(P, "rb").read()
CRLF = b"\r\n"
def S(x):  # str -> CRLF bytes
    return x.replace("\n", "\r\n").encode("utf-8")

edits = []

# 1. New section: Arabic labelling (before "Why Applications Get Rejected")
old = S("  <h2>Why Applications Get Rejected</h2>")
new = S("""  <h2>Arabic Labelling and Marking</h2>
  <p>Labelling is where otherwise-complete applications fail. Saudi requirements for ventilating fans centre on bilingual, accurate, traceable marking:</p>
  <ul>
    <li><strong>Bilingual ratings label.</strong> Model number, voltage, frequency (60 Hz), power input and manufacturer details on the ratings plate, with Arabic text alongside English. Translate the descriptive text &mdash; the model code itself stays unchanged so it matches the SABER record.</li>
    <li><strong>Country of origin.</strong> &ldquo;Made in China&rdquo; must appear on the product and on export cartons, in Arabic and English.</li>
    <li><strong>Importer details.</strong> Saudi authorities expect the local importer&rsquo;s name and commercial registration on packaging or accompanying documentation for regulated goods.</li>
    <li><strong>Arabic safety warnings.</strong> Any warning or installation notice printed on the product or carton needs an Arabic version.</li>
    <li><strong>GCTS marking.</strong> Units covered by a G-Mark must carry the GCTS traceability mark exactly as specified on the certificate.</li>
  </ul>
  <div class="note">
    <p><strong>Fix the artwork before mass production.</strong> Label artwork is reviewed as part of the PCoC file. Changing a printed label after production means re-submission &mdash; and in the worst case re-testing. Send the artwork draft together with the technical file, not after the goods are packed.</p>
  </div>
  <p>BAER prepares bilingual (Arabic/English) ratings label artwork and carton marking per model for Saudi consignments, matched to the importer&rsquo;s registered details.</p>

  <h2>Sequencing Certification with Your Order</h2>
  <p>Certification does not need to delay production if it starts at the right moment:</p>
  <ol class="steps">
    <li><strong>At PO confirmation.</strong> Request the technical file immediately. CB report validity, G-Mark status and label artwork are all checked now &mdash; not after production.</li>
    <li><strong>While production runs.</strong> The importer registers the model on SABER and the CAB reviews the file for the PCoC. Typical CAB processing is 5&ndash;15 working days with a complete file.</li>
    <li><strong>Before the vessel departs.</strong> Apply for the SCoC with the final commercial invoice, packing list and bill of lading. Never wait for arrival &mdash; a SCoC cannot be backdated.</li>
    <li><strong>On the calendar.</strong> The PCoC renews every 12 months and the G-Mark every 3 years. Repeat importers should track both; an expired certificate discovered mid-order stops the shipment.</li>
  </ol>

  <h2>Why Applications Get Rejected</h2>""")
edits.append(("insert labelling+sequencing", b.count(old), 1, old, new))

# 2. "What BAER Supplies" closing: add RFQ + Arabic links
old = S("""before you commit to a shipment date. See also our <a href="/saudi-arabia-exhaust-fan-supplier" style="color:#C0392B;font-weight:700;">Saudi Arabia supply page</a> for product recommendations by application.</p>""")
new = S("""before you commit to a shipment date. For a complete requirements checklist, use our <a href="/exhaust-fan-rfq-template" style="color:#C0392B;font-weight:700;">exhaust fan RFQ template</a>. See also our <a href="/saudi-arabia-exhaust-fan-supplier" style="color:#C0392B;font-weight:700;">Saudi Arabia supply page</a> for product recommendations by application, and its <a href="/ar/saudi-arabia-exhaust-fan-supplier" style="color:#C0392B;font-weight:700;">Arabic version</a> for Arabic-speaking procurement teams.</p>""")
edits.append(("RFQ+ar links", b.count(old), 1, old, new))

# 3. Visible FAQ: 3 new items before closing </div> of faq block
old = S("""    <h3 style="margin-top:18px;">Who is responsible for obtaining the certificates?</h3>
    <p>The Saudi importer registers on SABER and applies for both certificates, since they are tied to the importer's commercial registration. The manufacturer supplies the supporting technical file — CB report, G-Mark, EMC reports, photos, label artwork and ISO documentation.</p>
  </div>""")
new = S("""    <h3 style="margin-top:18px;">Who is responsible for obtaining the certificates?</h3>
    <p>The Saudi importer registers on SABER and applies for both certificates, since they are tied to the importer's commercial registration. The manufacturer supplies the supporting technical file — CB report, G-Mark, EMC reports, photos, label artwork and ISO documentation.</p>
    <h3 style="margin-top:18px;">Can we use our existing CE test reports for SABER?</h3>
    <p>Not directly. CE marking for fans is typically a self-declaration route, while SABER applications are built on CB-scheme reports and certificates. Reports generated for CE purposes can be a useful base, but the CAB will normally require CB-format documentation covering the 60 Hz national deviation. Confirm with the CAB before assuming existing reports transfer.</p>
    <h3 style="margin-top:18px;">How far in advance should certification start?</h3>
    <p>Start at PO confirmation. Requesting the technical file immediately, and letting the importer register on SABER while production runs, means the PCoC is typically in place before the goods are packed &mdash; and the SCoC can be applied for as soon as the shipping documents are final.</p>
    <h3 style="margin-top:18px;">Does SABER certification need renewing?</h3>
    <p>Yes. The PCoC is valid for 12 months and must be renewed annually, the SCoC is issued per shipment, and the G-Mark is valid for 3 years. Renewals are usually straightforward as long as the underlying test reports are still within their validity window.</p>
  </div>""")
edits.append(("visible FAQ x3", b.count(old), 1, old, new))

# 4. Dates
old = S("Last updated: September 8, 2026")
new = S("Last updated: November 18, 2026")
edits.append(("last updated line", b.count(old), 1, old, new))

# 5. FAQ JSON-LD sync
m = None
import re
for mm in re.finditer(rb'<script type="application/ld\+json">([^<]*"FAQPage"[^<]*)</script>', b):
    m = mm
if not m:
    print("FATAL: FAQ JSON-LD not found"); sys.exit(1)
faq = json.loads(m.group(1).decode("utf-8").strip())
names = [q["name"] for q in faq["mainEntity"]]
add = [
 {"@type":"Question","name":"Can we use our existing CE test reports for SABER?","acceptedAnswer":{"@type":"Answer","text":"Not directly. CE marking for fans is typically a self-declaration route, while SABER applications are built on CB-scheme reports and certificates. Reports generated for CE purposes can be a useful base, but the CAB will normally require CB-format documentation covering the 60 Hz national deviation."}},
 {"@type":"Question","name":"How far in advance should certification start?","acceptedAnswer":{"@type":"Answer","text":"Start at PO confirmation. Requesting the technical file immediately, and letting the importer register on SABER while production runs, means the PCoC is typically in place before the goods are packed, and the SCoC can be applied for as soon as the shipping documents are final."}},
 {"@type":"Question","name":"Does SABER certification need renewing?","acceptedAnswer":{"@type":"Answer","text":"Yes. The PCoC is valid for 12 months and must be renewed annually, the SCoC is issued per shipment, and the G-Mark is valid for 3 years. Renewals are usually straightforward as long as the underlying test reports are still within their validity window."}},
]
for q in add:
    if q["name"] in names:
        print("skip dup FAQ:", q["name"]); continue
    faq["mainEntity"].append(q)
faq_ld = S('<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + '</script>')
edits.append(("FAQ JSON-LD", 1, 1, m.group(0), faq_ld))

# 6. dateModified
old = b'"dateModified": "2026-11-12"'
new = b'"dateModified": "2026-11-18"'
edits.append(("dateModified", b.count(old), 1, old, new))

# apply
for name, cnt, expect, old, new in edits:
    print(f"[dry-run] {name}: occurrences={cnt} expected={expect}")
    if cnt != expect:
        print(f"FATAL: {name} count mismatch"); sys.exit(1)
for name, cnt, expect, old, new in edits:
    b = b.replace(old, new, 1)
    print(f"[applied] {name}")
open(P, "wb").write(b)
print("saved", len(b), "bytes")

# verify
b2 = open(P, "rb").read()
assert b2.count(b"\r\r\n") == 0, "double CR!"
faqs = json.loads(re.search(rb'<script type="application/ld\+json">([^<]*"FAQPage"[^<]*)</script>', b2).group(1).decode("utf-8").strip())
print("FAQ questions:", len(faqs["mainEntity"]))
body = re.sub(rb'<script.*?</script>|<style.*?</style>', b'', b2, flags=re.S)
body = re.sub(rb'<[^>]+>', b' ', body)
print("word count approx:", len(body.split()))
for tag in ["div","section","ul","li","h2","h3","p","a","table","tr","td","th","ol","figure","figcaption"]:
    o = len(re.findall((r'<%s[\s>]' % tag).encode(), b2)); c = len(re.findall(("</%s>" % tag).encode(), b2))
    if o != c: print(f"TAG-IMBALANCE {tag}: {o}/{c}")
print("verify done")
