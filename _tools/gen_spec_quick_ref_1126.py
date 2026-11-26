# -*- coding: utf-8 -*-
"""Create the cross-family specification quick-reference page (AEO data card).

Data source: numbers copied verbatim from already-live pages
  - KLT table: klt-series-panel-exhaust-fan.html (Full KLT Series Specifications)
  - BXF: inline-duct-fans.html (BXF-100..315 airflow figures)
  - FA: industrial-exhaust-fans.html (FA8-20..FA16-40)
Idempotent: if the page / links already exist, SKIP.

Usage:
  python _tools/gen_spec_quick_ref_1126.py           # dry-run
  python _tools/gen_spec_quick_ref_1126.py --apply   # write
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLY = "--apply" in sys.argv
PAGE = "exhaust-fan-model-spec-quick-reference.html"
URL = "https://baer-ventilation.com/exhaust-fan-model-spec-quick-reference"
TITLE = "Exhaust Fan Model Specification Quick Reference | BAER"
DESC = ("BAER KLT panel, BXF inline and FA axial fan specs side by side: size, airflow, power, "
        "voltage, noise, packing and MOQ in one factory-direct table.")

# ---- KLT data (verbatim from live klt-series page) ----
KLT = [
    ("KLT-10B", '6"', "200×200", "160×160", "Φ85", "220/50", "30 W", "150 m³/h", "1200 r/min", "35 dB", "20 / 0.108 / 18.05"),
    ("KLT-12B", '8"', "250×250", "205×205", "Φ100", "220/50", "30 W", "380 m³/h", "1200 r/min", "38 dB", "12 / 0.142 / 14.55"),
    ("KLT-18B", '10"', "310×310", "245×245", "Φ100", "220/50", "40 W", "432 m³/h", "1130 r/min", "42 dB", "10 / 0.172 / 16.00"),
    ("KLT-20B", '12"', "340×340", "290×290", "Φ100", "220/50", "80 W", "792 m³/h", "1100 r/min", "45 dB", "8 / 0.189 / 16.70"),
    ("KLT-25B", '14"', "400×400", "330×330", "Φ150", "220/50", "120 W", "1500 m³/h", "650 r/min", "48 dB", "4 / 0.157 / 12.50"),
    ("KLT-30B", '18"', "600×600", "480×480", "Φ150", "220/50", "120 W", "1800 m³/h", "685 r/min", "48 dB", "1 / 0.118 / 6.25"),
]
# ---- BXF data (verbatim from live inline-duct-fans page) ----
BXF = [
    ("BXF-100", "100 mm", "290 m³/h"),
    ("BXF-125", "125 mm", "420 m³/h"),
    ("BXF-150", "150 mm", "620 m³/h"),
    ("BXF-200", "200 mm", "1,200 m³/h"),
    ("BXF-250", "250 mm", "—"),
    ("BXF-315", "315 mm", "2,200 m³/h"),
]

FAQ = [
    ("What exhaust fan models does BAER make?",
     "BAER makes three families: KLT wall/panel exhaust fans in six sizes (6 to 18 inch, 150 to 1,800 m³/h), "
     "BXF inline duct fans from 100 to 315 mm, and FA axial fans from FA8-20 to FA16-40. All are factory-direct "
     "from our Shengzhou, China facility."),
    ("Which KLT model gives the most airflow?",
     "The KLT-30B (18 inch) delivers 1,800 m³/h at 120 W, followed by the KLT-25B (14 inch) at 1,500 m³/h. "
     "The smallest, KLT-10B (6 inch), moves 150 m³/h at 30 W. All KLT models are 220 V / 50 Hz as standard."),
    ("What is the minimum order quantity?",
     "The standard MOQ is 100 pieces per model, for both stock and OEM/custom orders."),
    ("What voltages are available?",
     "KLT panel fans are 220 V / 50 Hz as standard. 110 V / 60 Hz and other voltages are available on OEM orders. "
     "For Gulf markets we specify 60 Hz variants; Saudi Arabia is the only 60 Hz Gulf market."),
    ("What certifications do BAER fans hold?",
     "CE (XH2601E0321945GC), CCC (2024010702612682), ISO 9001 (04625Q15304R1M) and ETL (5024594, no expiry date "
     "stated). CB reports are available; SASO/SABER PCoC is issued per shipment and G-Mark on request. "
     "Certificates cover specific models and voltages - ask for the ones matching your order. SAA renewal is "
     "arranged per AU/NZ order; the previous certificate lapsed in September 2026."),
    ("Can I get the net weight for customs declaration?",
     "Packing data is shown per export carton (pieces / CBM / gross weight). Net weight depends on motor winding, "
     "cable length and plug type, so it is confirmed on the packing list for each order. Contact us if you need it "
     "for a customs declaration."),
]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build_page():
    klt_rows = "\n".join(
        "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
        % tuple(esc(x) for x in r) for r in KLT)
    bxf_rows = "\n".join(
        "<tr><td><strong>%s</strong></td><td>%s</td><td>%s</td><td><a href=\"/inline-duct-fans\">Full BXF range →</a></td></tr>"
        % tuple(esc(x) for x in r) for r in BXF)
    faq_items = "\n".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (esc(q), esc(a)) for q, a in FAQ)
    schema_faq = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    schema_web = json.dumps({"@context": "https://schema.org", "@type": "WebPage",
        "name": TITLE, "description": DESC, "url": URL,
        "about": {"@type": "Organization", "@id": "https://baer-ventilation.com/#organization",
                  "name": "BAER Ventilation", "legalName": "Zhejiang Baer Electrical Technology Co.,ltd",
                  "url": "https://baer-ventilation.com/"},
        "inLanguage": "en", "dateModified": "2026-11-26"}, ensure_ascii=False)
    schema_bc = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "@id": URL + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://baer-ventilation.com/"},
            {"@type": "ListItem", "position": 2, "name": "Resources", "item": "https://baer-ventilation.com/resources"},
            {"@type": "ListItem", "position": 3, "name": "Specification Quick Reference", "item": URL}]}, ensure_ascii=False)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y7GNF2D0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date()); gtag('config', 'G-0Y7GNF2D0H');
</script>
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="max-image-preview:large">
<link rel="canonical" href="%(url)s">
<link rel="alternate" hreflang="en" href="%(url)s">
<link rel="alternate" hreflang="x-default" href="%(url)s">
<meta property="og:type" content="article">
<meta property="og:site_name" content="BAER Ventilation">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="https://baer-ventilation.com/images/baer-factory-gate.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="900">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">%(web)s</script>
<script type="application/ld+json">%(bc)s</script>
<script type="application/ld+json">%(faq)s</script>
<style>
  .hero{background:linear-gradient(135deg,#0f1f3d 0%%,#1a3a6b 100%%);color:#fff;padding:70px 20px 55px;text-align:center}
  .hero h1{font-size:clamp(22px,3.5vw,38px);font-weight:800;margin:0 0 14px;max-width:880px;margin-left:auto;margin-right:auto}
  .hero p{color:#CBD5E1;font-size:15px;max-width:740px;margin:0 auto}
  .body{max-width:1120px;margin:0 auto;padding:50px 20px 80px}
  .body h2{font-size:23px;font-weight:800;color:#1E293B;margin:46px 0 14px;border-left:4px solid #C0392B;padding-left:14px}
  .body p,.body li{color:#475569;font-size:15px;line-height:1.85}
  .lead{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:18px 22px;margin:0 0 26px}
  .table-scroll{overflow-x:auto;margin:20px 0}
  table{width:100%%;border-collapse:collapse;font-size:13px;min-width:980px}
  th{background:#0f1f3d;color:#fff;text-align:left;padding:10px 9px;white-space:nowrap}
  td{padding:9px;border-bottom:1px solid #E2E8F0;color:#475569;white-space:nowrap}
  tbody tr:nth-child(even){background:#F8FAFC}
  .note{font-size:13px;color:#64748B;margin-top:10px}
  details{border:1px solid #E2E8F0;border-radius:8px;padding:14px 18px;margin:10px 0;background:#fff}
  summary{font-weight:700;color:#1E293B;cursor:pointer}
  details p{margin:12px 0 0}
  .cta{background:#0f1f3d;color:#fff;border-radius:12px;padding:28px;margin:44px 0 0;text-align:center}
  .cta a{display:inline-block;background:#C0392B;color:#fff;padding:11px 22px;border-radius:5px;text-decoration:none;font-weight:700;margin:6px}
  a{color:#1a3a6b}
</style>
</head>
<body>
<header></header>
<main>
<section class="hero">
  <h1>Exhaust Fan Model Specification Quick Reference</h1>
  <p>KLT panel, BXF inline duct and FA axial fans — size, airflow, power, voltage, noise and packing facts in one table. Factory-direct data from BAER's Shengzhou facility.</p>
</section>
<div class="body">
  <div class="lead"><strong>At a glance:</strong> BAER makes three fan families. <strong>KLT</strong> wall/panel fans: 6 models, 6–18 inch, 150–1,800 m³/h. <strong>BXF</strong> inline duct fans: 100–315 mm. <strong>FA</strong> axial fans: FA8-20 to FA16-40. Standard MOQ 100 pcs per model. Standard KLT voltage 220 V / 50 Hz, with 110 V / 60 Hz and other voltages on OEM order.</div>

  <h2>KLT Panel Exhaust Fans — Full Specification Table</h2>
  <p>Six models, one motor family. All 220 V / 50 Hz as standard; 110 V / 60 Hz and other voltages available on OEM orders.</p>
  <div class="table-scroll">
  <table>
    <thead><tr><th>Model</th><th>Panel (mm)</th><th>Cut-out (mm)</th><th>Outlet</th><th>V/Hz</th><th>Power</th><th>Airflow</th><th>Speed</th><th>Noise</th><th>Pcs/CBM/G.W.(kg)</th></tr></thead>
    <tbody>
%(klt_rows)s
    </tbody>
  </table>
  </div>
  <p class="note">Panel Size = front plate dimensions. Install Size (cut-out) = wall opening. Outlet = duct connection diameter. CBM and G.W. are per export carton. Net weight depends on motor winding, cable length and plug type, confirmed on each order's packing list. Data: <a href="/klt-series-panel-exhaust-fan">KLT series page</a>.</p>

  <h2>BXF Inline Duct Fans — Airflow by Size</h2>
  <p>BXF mixed-flow inline fans duct from 100 mm to 315 mm. Full construction, pressure and installation detail is on the inline duct fans guide.</p>
  <div class="table-scroll">
  <table style="min-width:520px">
    <thead><tr><th>Model</th><th>Duct size</th><th>Airflow</th><th>Detail</th></tr></thead>
    <tbody>
%(bxf_rows)s
    </tbody>
  </table>
  </div>
  <p class="note">Full BXF specifications and selection: <a href="/inline-duct-fans">Inline Duct Fans: The Complete Guide</a>.</p>

  <h2>FA Axial Fans — Range</h2>
  <p>The FA axial family covers FA8-20 to FA16-40 for industrial and commercial ventilation. For ACH tables, warehouse and workshop sizing, see the industrial exhaust fans guide. BAER does not publish a per-model axial table here — send your airflow and duct requirements for a factory quote.</p>
  <p><a href="/industrial-exhaust-fans">Industrial Exhaust Fans →</a> · <a href="/exhaust-fans">All fan types →</a></p>

  <h2>How to Read These Numbers</h2>
  <ul>
    <li><strong>Inch is a mounting size, not airflow.</strong> A 6 inch KLT moves 150 m³/h while a 6 inch inline can move far more — compare m³/h, not the inch label. See the <a href="/exhaust-fan-sizes-guide">sizes guide</a>.</li>
    <li><strong>Size by air changes per hour (ACH), not guesswork.</strong> Bathrooms need 8–12 ACH, kitchens 15–20. Use the <a href="/cfm-calculator">CFM calculator</a> or the <a href="/exhaust-fan-airflow-calculation-guide">airflow calculation guide</a>.</li>
    <li><strong>Noise is dB(A) at the rated point.</strong> For sones and dB comparison see the <a href="/exhaust-fan-noise-levels-guide">noise levels guide</a>.</li>
    <li><strong>Certificates cover specific models and voltages.</strong> Verify the exact ones for your order on the <a href="/verify">verification page</a>.</li>
  </ul>

  <h2>Certifications &amp; Factory Facts</h2>
  <p>Zhejiang Baer Electrical Technology Co.,ltd (brand: BAER Ventilation), Shengzhou, China. Legal entity registered September 2017, factory heritage since 2003. CE (XH2601E0321945GC), CCC (2024010702612682), ISO 9001 (04625Q15304R1M) and ETL (5024594) on file. Annual capacity 1,000,000 units. MOQ 100 pcs per model. Prices quoted per configuration. See <a href="/baer-production-capacity">production capacity</a> and <a href="/saber-saso-exhaust-fan-certification">SABER/SASO guide</a>.</p>

  <h2>Frequently Asked Questions</h2>
%(faq_items)s

  <div class="cta">
    <h2 style="color:#fff;border:none;margin:0 0 10px">Need a model matched to your room and voltage?</h2>
    <p style="color:#CBD5E1">Send room size, mounting type and target market — we return an itemised quote within 24 hours.</p>
    <a href="/exhaust-fan-rfq-template">Get the RFQ template</a>
    <a href="/contact/">Contact BAER</a>
  </div>
</div>
</main>
<footer></footer>
</body>
</html>
""" % dict(title=TITLE, desc=DESC, url=URL, web=schema_web, bc=schema_bc, faq=schema_faq,
           klt_rows=klt_rows, bxf_rows=bxf_rows, faq_items=faq_items)

# ---- write rules: page + sitemap + llms.txt + resources card + 2 inbound links ----
def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")

RULES = [
    (PAGE, None, build_page(), "create quick-reference page"),
    ("sitemap.xml",
     "  </urlset>",  # placeholder, replaced below
     "", "placeholder"),
]

changes = []
# 1) page
p = os.path.join(ROOT, PAGE)
if os.path.exists(p):
    changes.append(("SKIP", PAGE, "already exists"))
else:
    changes.append(("ADD", PAGE, "%d bytes" % len(build_page().encode("utf-8"))))
    if APPLY:
        open(p, "wb").write(crlf(build_page()))

# 2) sitemap: insert before </urlset>
sp = os.path.join(ROOT, "sitemap.xml")
sdata = open(sp, "rb").read()
sitemap_entry = ("  <url>\r\n    <loc>%s</loc>\r\n    <lastmod>2026-11-26</lastmod>\r\n  </url>\r\n" % URL).encode("utf-8")
needle = b"</urlset>"
if URL.encode() in sdata:
    changes.append(("SKIP", "sitemap.xml", "URL already present"))
elif sdata.count(needle) != 1:
    changes.append(("FAIL", "sitemap.xml", "closing tag not unique (%d)" % sdata.count(needle)))
else:
    changes.append(("ADD", "sitemap.xml", "1 URL entry"))
    if APPLY:
        open(sp, "wb").write(sdata.replace(needle, sitemap_entry + needle, 1))

# 3) llms.txt: add one line under Tools
lp = os.path.join(ROOT, "llms.txt")
ldata = open(lp, "rb").read()
llms_line = ("- [Specification Quick Reference](%s): side-by-side KLT panel, BXF inline and FA axial model specs — "
             "size, airflow, power, voltage, noise, packing and MOQ in one table.\r\n" % URL).encode("utf-8")
anchor = b"- [CFM Calculator](https://baer-ventilation.com/cfm-calculator)"
if URL.encode() in ldata:
    changes.append(("SKIP", "llms.txt", "URL already present"))
elif ldata.count(anchor) != 1:
    changes.append(("FAIL", "llms.txt", "anchor not unique (%d)" % ldata.count(anchor)))
else:
    changes.append(("ADD", "llms.txt", "1 line"))
    if APPLY:
        # insert after the full CFM calculator line (ends at next \r\n)
        idx = ldata.index(anchor)
        eol = ldata.index(b"\r\n", idx) + 2
        open(lp, "wb").write(ldata[:eol] + llms_line + ldata[eol:])

# 4) resources card
rp = os.path.join(ROOT, "resources.html")
rdata = open(rp, "rb").read()
card = ('<article class="card"><span class="tag">Specification</span><h2>Exhaust Fan Model Specification Quick Reference</h2>'
        '<p>KLT panel, BXF inline and FA axial fan specs side by side: size, airflow, power, voltage, noise, packing and MOQ in one table.</p>'
        '<a href="/exhaust-fan-model-spec-quick-reference">Open the spec quick reference →</a></article>\r\n').encode("utf-8")
ranchor = b'<article class="card"><span class="tag">Technical</span><h2>GB 29539-2025 Energy Efficiency Standard</h2>'
if b"/exhaust-fan-model-spec-quick-reference" in rdata:
    changes.append(("SKIP", "resources.html", "card already present"))
elif rdata.count(ranchor) != 1:
    changes.append(("FAIL", "resources.html", "anchor not unique (%d)" % rdata.count(ranchor)))
else:
    changes.append(("ADD", "resources.html", "1 card"))
    if APPLY:
        open(rp, "wb").write(rdata.replace(ranchor, card + ranchor, 1))

# 5) inbound link from airflow guide (highest ChatGPT landing page)
ap = os.path.join(ROOT, "exhaust-fan-airflow-calculation-guide.html")
adata = open(ap, "rb").read()
link_html = ('<p class="note">Looking for the exact size, power and packing of a specific model? '
             'See the <a href="/exhaust-fan-model-spec-quick-reference">model specification quick reference</a>.</p>\r\n').encode("utf-8")
# adapt to the file's own newline style and keep the anchor's leading indent
_nl = b"\r\n" if adata.count(b"\r\n") > adata.count(b"\n") / 2 else b"\n"
aanchor = b'  <h2 id="related-guides">Related Guides</h2>'
link_line = ('  <p class="note">Looking for the exact size, power and packing of a specific model? '
             'See the <a href="/exhaust-fan-model-spec-quick-reference">model specification quick reference</a>.</p>'
             ).encode("utf-8") + _nl
if b"/exhaust-fan-model-spec-quick-reference" in adata:
    changes.append(("SKIP", "exhaust-fan-airflow-calculation-guide.html", "link already present"))
elif adata.count(aanchor) != 1:
    changes.append(("FAIL", "exhaust-fan-airflow-calculation-guide.html", "anchor not unique (%d)" % adata.count(aanchor)))
else:
    changes.append(("ADD", "exhaust-fan-airflow-calculation-guide.html", "1 inbound link"))
    if APPLY:
        open(ap, "wb").write(adata.replace(aanchor, link_line + aanchor, 1))

print("=== %s ===" % ("APPLY" if APPLY else "DRY-RUN"))
for act, f, note in changes:
    print("  [%s] %-48s %s" % (act, f, note))
fails = [c for c in changes if c[0] == "FAIL"]
print("FAIL anchors:", len(fails))
sys.exit(1 if fails else 0)
