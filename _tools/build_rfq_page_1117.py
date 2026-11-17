# -*- coding: utf-8 -*-
"""Build /exhaust-fan-rfq-template per 选题池 (2026-11-16 P1). CRLF output. Idempotent."""
import os, io, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "exhaust-fan-rfq-template.html")

TITLE = "Exhaust Fan RFQ Template: 20 Questions to Ask a Supplier | BAER"
DESC = ("A ready-to-copy exhaust fan RFQ template with 20 specifications - airflow, static "
        "pressure, voltage, motor, mounting and certification - plus a free download.")

LEAD = ("Send an exhaust fan RFQ that gets a usable quote back the first time. This template lists the "
        "20 specifications a factory needs to size a fan, confirm compliance and quote accurately — "
        "copy the checklist below or download the text file and fill it in.")

# Section texts kept as constants so word count is measurable.
S_INTRO = """<p>Most RFQs sent to exhaust fan factories stall for the same reason: the buyer specifies a fan by appearance or by a model number found on a competitor's catalogue, and omits the four values that actually determine the fan — airflow, static pressure, voltage and mounting. The factory cannot quote from a photograph, so it replies with questions, and two weeks pass before a number arrives. A structured request removes that round trip.</p>
<p>This page is the checklist BAER uses internally when a customer asks for a quotation. It works for panel, window, ceiling, inline duct and axial fans, and it works whether you are buying 100 units or a container. You do not need to fill in every line. Mark unknown items "TBC" — an honest blank is more useful to an engineer than a guessed figure, because it tells us what to propose rather than what to copy.</p>"""

S_WHY = """<h2 id="why-structured">Why a structured RFQ gets a faster quote</h2>
<p>A fan is selected by a duty point, not by a catalogue picture. Two fans with the same 200 mm impeller can move very different volumes of air depending on blade pitch, motor speed and system resistance. If you request "a 200 mm exhaust fan" without airflow or pressure, a supplier can only quote a generic model, and the price will change once the real duty point is known. Specifying the duty point up front turns a vague inquiry into a manufacturable order.</p>
<p>There is a second reason. Certification and voltage are market-specific. A 220–240 V / 50 Hz fan with a CE-marked motor is not automatically suitable for a 110–120 V / 60 Hz installation, and a fan destined for Saudi Arabia may need a different documentation set from one going to Germany. Stating the destination country in the first line lets the factory confirm compliance before quoting, not after the proforma invoice.</p>
<p>Finally, an RFQ is a record. When the specification lives in one document, both sides can refer back to it when a sample is tested or a shipment is inspected. That matters more in OEM work, where logo, carton and plug type are easy to get wrong if they were only mentioned in a chat message.</p>"""

S_20 = """<h2 id="the-20-items">The 20 items to include in your exhaust fan RFQ</h2>
<p>The table below is ordered the way a factory reads it. Items 1–7 identify the buyer and the destination, items 8–14 define the fan itself, and items 15–20 cover compliance, branding and delivery. Every line has a short note explaining why it matters, so you can decide what to leave blank.</p>
<div class="table-scroll">
<table class="compare-table">
<thead><tr><th>#</th><th>Item to specify</th><th>Example</th><th>Why the factory needs it</th></tr></thead>
<tbody>
<tr><td>1</td><td><strong>Company name</strong></td><td>Your import company, registered name</td><td>Quotations, proforma invoices and shipping documents are issued to this name.</td></tr>
<tr><td>2</td><td><strong>Contact and email</strong></td><td>Name, direct email, WhatsApp</td><td>One named contact avoids replies going to a general mailbox.</td></tr>
<tr><td>3</td><td><strong>Destination country and port</strong></td><td>Jeddah, Saudi Arabia / Hamburg, Germany</td><td>Determines voltage, plug, certification and documentation.</td></tr>
<tr><td>4</td><td><strong>Quantity per model</strong></td><td>500 pcs KLT-12B, 300 pcs FA-20</td><td>Toolin, packing and production planning are per model, not per order.</td></tr>
<tr><td>5</td><td><strong>Fan type</strong></td><td>Panel / window / ceiling / inline / axial</td><td>Different families use different housings and motors.</td></tr>
<tr><td>6</td><td><strong>Impeller diameter</strong></td><td>200 mm or 8 inch</td><td>First sizing filter; state metric or imperial so nothing is converted twice.</td></tr>
<tr><td>7</td><td><strong>Airflow required</strong></td><td>600 m3/h (350 CFM)</td><td>The primary performance value; give units, not just a number.</td></tr>
<tr><td>8</td><td><strong>Static pressure</strong></td><td>60 Pa at the duty point</td><td>Ducted systems need pressure capability, not only free-air airflow.</td></tr>
<tr><td>9</td><td><strong>Voltage and frequency</strong></td><td>220–240 V / 50 Hz or 110–120 V / 60 Hz</td><td>Motor winding and plug are built to this line.</td></tr>
<tr><td>10</td><td><strong>Motor type</strong></td><td>Shaded pole, ball bearing, or EC</td><td>Affects noise, life, efficiency and configuration cost.</td></tr>
<tr><td>11</td><td><strong>Mounting position</strong></td><td>Wall / window / ceiling / duct inline</td><td>Changes the housing, shutter and fixing method.</td></tr>
<tr><td>12</td><td><strong>Shutter type</strong></td><td>None / manual / automatic</td><td>Shutters add depth, weight and a separate part number.</td></tr>
<tr><td>13</td><td><strong>Noise limit</strong></td><td>Below 45 dB(A) at 1 m</td><td>Required for bathrooms, hotels and bedrooms; affects blade design.</td></tr>
<tr><td>14</td><td><strong>IP rating</strong></td><td>IP44 for a bathroom zone</td><td>Determines enclosure and cable entry; state it if your market requires it.</td></tr>
<tr><td>15</td><td><strong>Operating environment</strong></td><td>Ambient 40 °C, humid, coastal</td><td>Coastal or high-heat sites may need different bearings or coatings.</td></tr>
<tr><td>16</td><td><strong>Certification required</strong></td><td>CE, CB (IEC 60335-2-80), CCC, ISO 9001</td><td>Test reports and certificate copies must match the destination market.</td></tr>
<tr><td>17</td><td><strong>HS code for your customs</strong></td><td>8414512000 for ≤125 W window/wall fans</td><td>Your broker may classify differently; agree the code before shipping.</td></tr>
<tr><td>18</td><td><strong>OEM / ODM details</strong></td><td>Logo, nameplate, colour box, plug type</td><td>Artwork and packaging are separate from the fan specification.</td></tr>
<tr><td>19</td><td><strong>Target delivery window</strong></td><td>Needed for Q1 project, flexible on date</td><td>Use a window or "flexible"; avoid fixing a date before the order is confirmed.</td></tr>
<tr><td>20</td><td><strong>Drawings, samples or references</strong></td><td>Existing model photo, duct layout drawing</td><td>A drawing resolves more ambiguity than a paragraph of description.</td></tr>
</tbody>
</table>
</div>
<p>Items 7 and 8 are the two most often left out, and the two most important. If you cannot calculate them, describe the room or duct instead — floor area, air changes per hour, duct length and number of bends — and the factory can propose a duty point for your confirmation.</p>"""

S_DOWNLOAD = """<h2 id="download">Download the RFQ template</h2>
<p>The checklist is also available as a plain text file you can paste into your email or save into your own purchasing system. No form, no registration.</p>
<div class="cta-box">
  <h3>Exhaust fan RFQ template (.txt)</h3>
  <p>20 fields, ready to copy. Works in any email client or spreadsheet.</p>
  <a href="/exhaust-fan-rfq-template.txt" class="btn-red" download>Download RFQ template</a>
</div>
<p>If you prefer to fill it in with us directly, send the same information through the <a href="/contact" style="color:#C0392B;font-weight:700;">contact page</a> or copy it into a WhatsApp message. We will return a completed specification sheet with the quotation so you can approve it line by line.</p>"""

S_SAMPLE = """<h2 id="sample">A filled-in example</h2>
<p>Here is how the same information looks when it is actually sent. This example is a hotel bathroom extraction project in Saudi Arabia; the numbers are illustrative and not a quotation.</p>
<div class="table-scroll">
<table class="compare-table">
<thead><tr><th>Field</th><th>Example entry</th></tr></thead>
<tbody>
<tr><td>Company / destination</td><td>Al-... Trading Co., Jeddah, Saudi Arabia — port: Jeddah Islamic Port</td></tr>
<tr><td>Quantity</td><td>800 pcs ceiling bathroom fan, 100 mm impeller</td></tr>
<tr><td>Duty point</td><td>85 m3/h free air, 35 Pa static, below 42 dB(A) at 1 m</td></tr>
<tr><td>Electrical</td><td>220–240 V / 50 Hz, ball-bearing motor, UK-style plug</td></tr>
<tr><td>Installation</td><td>Ceiling mount, ducted, automatic backdraft shutter</td></tr>
<tr><td>Compliance</td><td>CE and CB test reports required with quotation; confirm SASO documentation route</td></tr>
<tr><td>OEM</td><td>Customer logo on nameplate, neutral carton, 12-month warranty card</td></tr>
<tr><td>TBC</td><td>IP rating — please propose for a bathroom zone 2 location</td></tr>
</tbody>
</table>
</div>
<p>Notice what the example does <em>not</em> contain: no requested price and no demanded delivery date. Asking "what is your best price" without a duty point produces a number that cannot be checked. Asking for the specification first produces a quotation that can be compared fairly between factories — because every supplier is quoting the same fan.</p>"""

S_MISTAKES = """<h2 id="mistakes">Five mistakes that slow an RFQ down</h2>
<h3>1. Quoting by impeller size alone</h3>
<p>A 150 mm fan and another 150 mm fan can differ by a factor of two in airflow. Always add airflow and pressure, or describe the space and duct so they can be estimated.</p>
<h3>2. Mixing metric and imperial units</h3>
<p>Write both when there is doubt — "200 mm (8 inch)" and "600 m3/h (350 CFM)". A number without a unit is the single most common source of a wrong quotation.</p>
<h3>3. Leaving out the destination country</h3>
<p>Voltage, plug, label language and certification all follow the destination. "Middle East" is not specific enough; name the country and port.</p>
<h3>4. Guessing a specification you do not know</h3>
<p>Mark it "TBC — please propose". A guessed static pressure that is too low will fail on site; a blank invites the engineer to recommend the right value.</p>
<h3>5. Asking for price before confirming the model</h3>
<p>Price follows specification. Confirm the model, duty point and certification first, then compare quotations on that basis. Otherwise you are comparing different products.</p>"""

S_CALC = """<h2 id="derive">How to derive airflow if you do not know it</h2>
<p>You do not need a catalogued figure to write a useful RFQ. For a room, the simplest method is air changes per hour: multiply room length by width by height to get cubic metres, then multiply by the number of air changes your application needs. A small bathroom typically needs 8–10 air changes per hour; a commercial kitchen needs far more because it must remove heat and cooking vapour as well as odour. Divide the result by 60 to convert from hours to minutes, and you have a target airflow in m3/h.</p>
<p>For a ducted system, the fan must also overcome resistance. Every metre of duct, every bend and every filter or grille reduces airflow. If your RFQ only states free-air airflow, the fan may deliver far less once installed. Either state the static pressure you expect, or give the duct diameter, total length and number of bends and ask the supplier to propose a duty point. A longer duct with several elbows usually needs a higher-pressure mixed-flow or centrifugal fan rather than a simple axial type.</p>
<p>Both methods produce an estimate, and that is fine — the point of the RFQ is to start from a stated assumption that both sides can check. Mark the figure as "calculated, please confirm" so the factory knows to verify it rather than quote it as a fixed requirement. Our <a href="/exhaust-fan-airflow-calculation-guide" style="color:#C0392B;font-weight:700;">airflow calculation guide</a> works through the room-volume and duct methods with examples if you want the detail before sending your request.</p>"""

S_OEM = """<h2 id="oem">Extra items for an OEM or private-label RFQ</h2>
<p>If the fans will carry your brand, add four lines to the standard checklist. First, the logo artwork and where it goes — on the housing, on the nameplate or only on the carton. Second, the nameplate content, including your model number, voltage, frequency, power and the country-of-origin mark required by your customs. Third, the packaging: neutral brown carton or a printed colour box, and whether a barcode or label is needed. Fourth, the plug and cable: the plug standard, cable length and any approval mark on the cord.</p>
<p>These items do not change how the fan performs, but they change what leaves the factory and they are the most common source of a rejected shipment. State them in the RFQ even if your answer is "to be confirmed" — that way the supplier knows to send a mock-up before production rather than printing a guess. For branded programmes, ask for a pre-production sample of the nameplate and carton together with the fan sample.</p>
<p>OEM orders carry a different minimum quantity from stock models because artwork and packaging are made for one buyer. At BAER the stock MOQ is 100 pcs per model and the OEM MOQ is 500 pcs per model, with different models allowed to share one container. State clearly in your RFQ whether you are asking for a stock fan with a neutral carton or a fully customised version — the two are quoted differently and mixing them in one line causes confusion.</p>"""

S_NEXT = """<h2 id="next">What happens after you send it</h2>
<p>At BAER, a complete RFQ goes to the technical team first. If the duty point is clear, we return a proposed model with its performance data, the certification list and a factory-direct quotation. If a value is missing, we come back with a specific question — not a generic "please advise" — usually on the same working day.</p>
<p>Samples are available before a container order. A sample lets you measure noise and airflow in the actual installation, which is the only reliable way to confirm a bathroom or kitchen application. For OEM projects we can also send a mock-up of the nameplate and carton before mass production.</p>
<p>Our standard terms stay simple: MOQ 100 pcs per model for stock versions and 500 pcs per model for OEM customisation, with mixed models allowed in one container. We do not publish fixed pricing — a quotation is issued against your specification, because voltage, motor and packaging change the configuration. Use the <a href="/exhaust-fan-airflow-calculation-guide" style="color:#C0392B;font-weight:700;">airflow calculation guide</a> if you need to derive the duty point before writing your RFQ, or the <a href="/panel-exhaust-fan-sizing-guide" style="color:#C0392B;font-weight:700;">panel fan sizing guide</a> if you are choosing between impeller sizes.</p>"""

S_FAQ = """<h2 id="faq">Frequently asked questions</h2>
<h3>Do I need to know the static pressure?</h3>
<p>Not necessarily. If the fan discharges straight through a short wall opening, free-air airflow may be enough. If it connects to ductwork, give the duct length, diameter and number of bends, and we will estimate the system resistance for you.</p>
<h3>Can I send a photo of my current fan instead?</h3>
<p>Yes — include it with the RFQ. A photo identifies the type and mounting quickly, but it cannot show airflow or pressure, so add those or describe the application. Label photos with the model and quantity they refer to.</p>
<h3>Why is there no published price?</h3>
<p>A published fixed price assumes every unit is identical. A quotation is issued for your exact voltage, motor, certification and packaging. We issue the latter because a fan built for 110 V / 60 Hz is not the same product as one built for 220 V / 50 Hz.</p>
<h3>Which certifications should I ask for?</h3>
<p>Ask for what your market and customer require. BAER supplies CE, CB to IEC 60335-2-80, CCC and ISO 9001 documentation. Test reports and certificate copies accompany the quotation. For Saudi Arabia, confirm the current documentation route with your customs broker before placing the order.</p>
<h3>Can I mix several models in one RFQ?</h3>
<p>Yes, and it is usually more efficient. List each model as a separate line with its own quantity, airflow and voltage, then give one destination and one contact for the whole request.</p>"""

S_RELATED = """<h2 id="related">Related guides</h2>
<ul>
<li><a href="/exhaust-fan-airflow-calculation-guide" style="color:#C0392B;font-weight:700;">How to Calculate Exhaust Fan Airflow (CFM and m3/h)</a></li>
<li><a href="/panel-exhaust-fan-sizing-guide" style="color:#C0392B;font-weight:700;">Panel Exhaust Fan Sizing Guide</a></li>
<li><a href="/exhaust-fan-certifications-guide" style="color:#C0392B;font-weight:700;">Exhaust Fan Certifications Explained</a></li>
<li><a href="/exhaust-fan-container-loading-guide" style="color:#C0392B;font-weight:700;">Container Loading: How Many Exhaust Fans Fit in a 20GP / 40HQ</a></li>
<li><a href="/exhaust-fan-moq-guide" style="color:#C0392B;font-weight:700;">MOQ: What It Is and How to Work With It</a></li>
<li><a href="/baer-production-capacity" style="color:#C0392B;font-weight:700;">Inside the BAER Factory: Capacity &amp; Quality Control</a></li>
<li><a href="/contact" style="color:#C0392B;font-weight:700;">Request a Quote</a></li>
</ul>"""

FIG = [
    ("/images/baer-panel-fan-klt-front.webp", "KLT panel exhaust fan — state impeller size, airflow and voltage in the RFQ", 960, 720),
    ("/images/baer-inline-duct-fan-shelf.webp", "Inline duct fan range — ducted applications also need static pressure", 960, 720),
    ("/images/inline-impellers.webp", "Mixed-flow impellers — blade design changes airflow at the same diameter", 960, 720),
    ("/images/baer-fan-types-shelf.webp", "Fan families on the BAER shelf — panel, ceiling and inline types", 960, 720),
    ("/images/motor-test-bench.webp", "Motor test bench — voltage and frequency define the winding", 960, 720),
    ("/images/baer-hi-pot-test.webp", "Hi-pot test station — safety testing before a fan leaves the line", 960, 720),
    ("/images/baer-certificate-wall.webp", "Certificates on file — state which documents your market requires", 960, 720),
    ("/images/baer-export-cartons-stacked.webp", "Export cartons — OEM packaging and carton marks belong in the RFQ", 960, 720),
]

def figure(src, cap, w, h):
    alt = cap.replace("&", "&amp;")
    return ('<figure style="margin:26px 0;text-align:center;">\n'
            f'    <img src="{src}" alt="{alt}" width="{w}" height="{h}" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">\n'
            f'    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">{cap}</figcaption>\n'
            '</figure>')

def body_with_figures():
    # insert 8 figures between sections, keyed by section marker
    parts = [S_INTRO, FIG和图(0), S_WHY, FIG和图(1), S_20, FIG和图(2), FIG和图(3), S_DOWNLOAD,
             FIG和图(4), S_CALC, S_SAMPLE, FIG和图(5), S_OEM, S_MISTAKES, FIG和图(6), S_NEXT, FIG和图(7), S_FAQ, S_RELATED]
    return "\n\n".join(p for p in parts if p)

def FIG和图(i):
    return figure(*FIG[i])

ld = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": TITLE,
    "description": DESC,
    "url": "https://baer-ventilation.com/exhaust-fan-rfq-template",
    "about": {
        "@type": "Organization",
        "@id": "https://baer-ventilation.com/#organization",
        "name": "BAER Ventilation",
        "legalName": "Zhejiang Baer Electrical Technology Co.,ltd",
        "url": "https://baer-ventilation.com/"
    },
    "inLanguage": "en",
    "dateModified": "2026-11-17"
}

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y7GNF2D0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-0Y7GNF2D0H');
</script>
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="robots" content="max-image-preview:large">
<link rel="canonical" href="https://baer-ventilation.com/exhaust-fan-rfq-template">
<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/exhaust-fan-rfq-template">
<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/exhaust-fan-rfq-template">
<meta property="og:type" content="article">
<meta property="og:site_name" content="BAER Ventilation">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="https://baer-ventilation.com/exhaust-fan-rfq-template">
<meta property="og:image" content="https://baer-ventilation.com/images/baer-panel-fan-klt-front.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="900">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://baer-ventilation.com/images/baer-panel-fan-klt-front.webp">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(',', ':'))}</script>
<style>
  .hero {{ background: linear-gradient(135deg, #0f1f3d 0%, #1a3a6b 100%); color: #fff; padding: 80px 20px 60px; text-align: center; }}
  .hero h1 {{ font-size: clamp(22px, 3.5vw, 38px); font-weight: 800; margin: 0 0 16px; max-width: 780px; margin-left: auto; margin-right: auto; }}
  .hero p {{ color: #CBD5E1; font-size: 15px; max-width: 620px; margin: 0 auto; }}
  .body {{ max-width: 820px; margin: 0 auto; padding: 60px 20px 80px; }}
  .body h2 {{ font-size: 22px; font-weight: 800; color: #1E293B; margin: 48px 0 16px; border-left: 4px solid #C0392B; padding-left: 14px; }}
  .body p, .body li {{ color: #475569; font-size: 15px; line-height: 1.85; }}
  .body ul {{ padding-left: 20px; }}
  .body h3 {{ font-size: 17px; color: #1E293B; margin: 26px 0 8px; }}
  .compare-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 14px; }}
  .compare-table th {{ background: #0f1f3d; color: #fff; text-align: left; padding: 10px 12px; }}
  .compare-table td {{ padding: 9px 12px; border-bottom: 1px solid #E2E8F0; color: #475569; vertical-align: top; }}
  .table-scroll {{ overflow-x: auto; }}
  .cta-box {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 22px; margin: 28px 0; }}
  .cta-box h3 {{ margin: 0 0 8px; color: #1E293B; }}
  .cta-box p {{ margin: 0 0 14px; }}
  .btn-red {{ display: inline-block; background: #C0392B; color: #fff; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: 700; }}
  .baer-breadcrumb ol {{ list-style: none; display: flex; gap: 8px; padding: 0; margin: 0 0 18px; font-size: 13px; color: #94A3B8; justify-content: center; }}
  .baer-breadcrumb a {{ color: #CBD5E1; text-decoration: none; }}
  .bv-topbar {{ background: #0a1730; padding: 7px 20px; display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }}
  .bv-topbar a {{ color: #e8eaee; text-decoration: none; }}
  .bv-topbar .bv-mail, .bv-topbar .bv-tel {{ color: #c2c8d2; }}
  .bv-wa-btn {{ display: inline-flex; align-items: center; gap: 6px; background: #25D366; color: #fff !important; padding: 5px 14px; border-radius: 18px; font-weight: 600; }}
  @media (max-width:640px){{.bv-topbar .bv-mail,.bv-topbar .bv-tel{{display:none;}}.bv-topbar-in{{justify-content:center;padding:6px 12px;}}}}
</style>
</head>
<body>
<div class="bv-topbar">
        <div class="bv-topbar-in">
            <a class="bv-mail" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
            <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
                <span class="bv-tel">WhatsApp/WeChat: +86 136 5585 9122</span>
                <a class="bv-wa-btn" href="https://wa.me/8613655859122?text=Hello%20BAER%2C%20I%27d%20like%20to%20send%20an%20exhaust%20fan%20RFQ." target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" width="15" height="15"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.5A9.9 9.9 0 1 0 12.04 2Z"/></svg><span>WhatsApp</span></a>
            </div>
        </div>
    </div>

<header class="site-header">
  <div class="container" style="display:flex;align-items:center;justify-content:space-between;padding:16px 20px;">
    <a href="/" style="font-size:22px;font-weight:900;color:#C0392B;text-decoration:none;">BAER<span style="color:#1E293B;font-weight:400;font-size:14px;margin-left:6px;">VENTILATION</span></a>
    <nav style="display:flex;gap:24px;font-size:14px;font-weight:600;">
      <a href="/" style="color:#1E293B;text-decoration:none;">Home</a>
      <a href="/products/" style="color:#1E293B;text-decoration:none;">Products</a>
      <a href="/resources" style="color:#1E293B;text-decoration:none;">Resources</a>
      <a href="/#inquiry" style="background:#C0392B;color:#fff;padding:8px 18px;border-radius:5px;text-decoration:none;">Get Quote</a>
    </nav>
  </div>
</header>
<div class="hero">
  <nav class="baer-breadcrumb" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li class="sep" aria-hidden="true">/</li><li><a href="/resources">Resources</a></li><li class="sep" aria-hidden="true">/</li><li aria-current="page">Exhaust Fan RFQ Template</li></ol></nav>
  <h1>Exhaust Fan RFQ Template: 20 Questions to Ask a Supplier</h1>
  <p class="hero-fact" style="color:#ffffff;font-size:15px;line-height:1.7;max-width:720px;margin:14px auto 0;">BAER (Zhejiang Baer Electrical Technology Co.,ltd), a China exhaust fan manufacturer since 2003 — CE, CB and ISO 9001 certified, MOQ 100 pcs, samples in 3–7 days — shares the 20-item RFQ checklist below.</p>
  <p>{LEAD}</p>
  <p style="font-size:13px;color:#CBD5E1;margin:10px 0 0;">Last updated: November 17, 2026</p>
</div>
<div class="body">

{body_with_figures()}

  <div class="cta-box">
    <h3>Ready to send your specification?</h3>
    <p>Copy the 20-item checklist or download the template, then email it to sunny@zjbaer.com. Our export team replies within one working day.</p>
    <a href="/#inquiry" class="btn-red">Request a Quote</a>
  </div>
</div>
<footer style="background:#0f1f3d;color:#94A3B8;text-align:center;padding:32px 20px;font-size:13px;">
  <p style="margin:0;">© 2026 BAER Ventilation · <a href="/" style="color:#C0392B;text-decoration:none;">baer-ventilation.com</a>
      · <a href="https://www.youtube.com/@BAERVentilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">YouTube</a> · <a href="https://www.linkedin.com/company/baer-ventilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">LinkedIn</a></p>
  <p style="margin:14px 0 0;font-size:12px;opacity:.85;"><a href="/privacy/" style="color:inherit;text-decoration:underline;">Privacy Policy</a> &middot; <a href="/privacy/#cookies" style="color:inherit;text-decoration:underline;">Cookie Notice</a> &middot; <a href="/verify/" style="color:inherit;text-decoration:underline;">Verify Our Company</a></p>
</footer>
<!-- GA4 conversion events: WhatsApp / email / PDF catalog / phone / form -->
<script>
function _baerGtagCtx(){{ return {{ page_path: window.location.pathname, page_title: document.title }}; }}
document.addEventListener('click', function(e){{
  var t = e.target;
  while (t && t !== document.body && t.tagName !== 'A') {{ t = t.parentElement; }}
  if (!t || t.tagName !== 'A' || typeof gtag !== 'function') return;
  var href = t.getAttribute('href') || '';
  var ctx = _baerGtagCtx();
  ctx.link_text = (t.textContent || '').trim().slice(0, 120);
  ctx.link_url = href;
  if (/wa\.me|whatsapp/i.test(href)) {{ gtag('event', 'whatsapp_click', ctx); }}
  else if (href.indexOf('mailto:') === 0) {{ gtag('event', 'email_click', ctx); }}
  else if (/\.pdf(\?|$)/i.test(href)) {{ ctx.file_name = href.split('/').pop().split('?')[0]; gtag('event', 'catalog_download', ctx); }}
  else if (href.indexOf('tel:') === 0) {{ gtag('event', 'phone_click', ctx); }}
}});
</script>

<script src="/js/reveal.js?v=1" defer></script></body>
</html>
"""

# --- dry-run metrics before writing ---
import re, html as H
text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S)
text = H.unescape(re.sub(r"<[^>]+>", " ", text))
words = re.findall(r"\b[A-Za-z][A-Za-z'\-]+\b", text)
print("WORDS:", len(words))
print("DESC chars:", len(DESC))
print("TITLE chars:", len(TITLE))
print("IMAGES:", html.count("<img "))
print("H1:", html.count("<h1"), "H2:", html.count("<h2"))
assert 2200 <= len(words) <= 3000, "word count out of range"
assert 130 <= len(DESC) <= 165, "desc out of range"
assert len(TITLE) <= 65, "title too long"
assert html.count("<img ") >= 8, "images < 8"
assert html.count("<h1") == 1

if "--apply" in __import__("sys").argv:
    io.open(OUT, "w", encoding="utf-8", newline="").write(html.replace("\n", "\r\n"))
    print("WROTE", OUT, os.path.getsize(OUT), "bytes")
else:
    print("DRY RUN — no write")
