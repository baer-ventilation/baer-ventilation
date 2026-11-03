# -*- coding: utf-8 -*-
"""Build /commercial-kitchen-exhaust-fans (BXF duct-fan led) from the industrial page shell."""
import io, re, json

SRC = 'industrial-exhaust-fans.html'
DST = 'commercial-kitchen-exhaust-fans.html'
SLUG = 'commercial-kitchen-exhaust-fans'
URL = 'https://baer-ventilation.com/' + SLUG

TITLE = 'Commercial Kitchen Exhaust Fans &mdash; Ducted BXF Series | BAER'
DESC = ('Ducted mixed-flow kitchen exhaust fans, 290&ndash;2,200 m&sup3;/h and up to 693 Pa, for cafe and '
        'restaurant extract runs, dishwash and make-up air. Sizing tables by kitchen type.')

s = io.open(SRC, encoding='utf-8', newline='').read()

# ---------- head ----------
s = s.replace('<title>Industrial Exhaust Fans for Warehouses &amp; Workshops | BAER</title>',
              '<title>' + TITLE + '</title>')
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="' + DESC + '">', s, count=1)
s = s.replace('<link rel="canonical" href="https://baer-ventilation.com/industrial-exhaust-fans">',
              '<link rel="canonical" href="' + URL + '">')
s = s.replace('<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/industrial-exhaust-fans">',
              '<link rel="alternate" hreflang="en" href="' + URL + '">')
s = s.replace('<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/industrial-exhaust-fans">',
              '<link rel="alternate" hreflang="x-default" href="' + URL + '">')
s = re.sub(r'<meta property="og:title" content="[^"]*">',
           '<meta property="og:title" content="' + TITLE + '">', s, count=1)
s = re.sub(r'<meta property="og:description" content="[^"]*">',
           '<meta property="og:description" content="Ducted mixed-flow kitchen exhaust fans from 290 to 2,200 m3/h, '
           'up to 693 Pa. Sizing by hood length, air changes and make-up air. Factory-direct, CE certified.">', s, count=1)
s = re.sub(r'<meta property="og:url" content="[^"]*">',
           '<meta property="og:url" content="' + URL + '">', s, count=1)
s = re.sub(r'<meta name="twitter:title" content="[^"]*">',
           '<meta name="twitter:title" content="Commercial Kitchen Exhaust Fans &mdash; Ducted BXF Series | BAER">', s, count=1)
s = re.sub(r'<meta name="twitter:description" content="[^"]*">',
           '<meta name="twitter:description" content="Mixed-flow duct fans 100-315 mm for kitchen extract and make-up air. '
           'Sizing tables by kitchen type, duct velocity and pressure budget.">', s, count=1)

# ---------- body ----------
BODY = u'''<section class="hero">
  <div class="hero-inner">
    <span class="hero-cat">Commercial Kitchen Ventilation</span>
    <h1>Commercial Kitchen Exhaust Fans: Ducted Mixed-Flow Systems</h1>
    <p>Kitchen extract fails for one of two reasons &mdash; the fan cannot hold pressure through the duct run, or nobody allowed for make-up air. BXF mixed-flow duct fans cover <strong>290&ndash;2,200 m&sup3;/h</strong> and up to <strong>693 Pa</strong> in six sizes from 100 to 315 mm, for cafe, restaurant, canteen and dishwash extract where the fan sits at the end of the run rather than in the wall.</p>
    <p style="font-size:13px;color:#64748B;margin:10px 0 0;">Last updated: November 3, 2026</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        WhatsApp Inquiry
      </a>
      <a class="btn btn-red" href="/contact/">Get a Quote</a>
      <a class="btn btn-ghost" href="/cfm-calculator">Airflow Calculator</a>
    </div>
  </div>
</section>

<div class="crumb">
  <a href="/">Home</a> / <a href="/products/">Products</a> / <span>Commercial Kitchen Exhaust Fans</span>
</div>

<div class="container">

  <p style="font-size:16.5px;line-height:1.8;max-width:900px;margin-bottom:44px;">A commercial kitchen is the hardest ventilation job in a building: hot, greasy, humid, and squeezed into a duct route that was designed after the building was. This page covers what a ducted mixed-flow fan can and cannot do in a kitchen, how to size the extract and the make-up air that has to replace it, and which BXF model matches each space &mdash; so the fan you order still delivers its rated airflow once the filter, the elbows and the wall louvre are in the way.</p>

  <h2 class="sec">First Question: Is the Air Grease-Laden?</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Light cooking, baffle filter fitted &mdash; BXF is right</h4><p>Electric hobs, ovens, microwaves, coffee and tea stations, warming lines. Grease load is low, a stainless baffle filter sits at the hood, and the duct fan goes downstream at the discharge end. This is the case this page is written for.</p></div>
      <div class="appcard"><h4>Deep fryers, wok ranges, charbroilers &mdash; BXF is not the right fan</h4><p>Heavy grease duty needs a welded grease duct, and a fan listed for grease service with the motor outside the airstream. The BXF motor sits in the airflow, so grease coating and cleaning access become a fire and failure risk. We will tell you this instead of shipping the wrong unit.</p></div>
  </div>
  <p style="max-width:900px;margin-top:22px;">If your kitchen is in the second group, say so on the enquiry and we will tell you what the duct route still needs &mdash; airflow, pressure and duct velocity are the same calculations either way, and the hood figures below still apply.</p>

  <span class="section-tag">MODEL MATCHING</span>
  <h2 class="sec">Which Model for Which Kitchen Space</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Staff canteen / tea room</h4><p>Reheat only, no frying. 8&ndash;10 air changes: <strong>BXF-150</strong> (620 m&sup3;/h) for up to 70 m&sup3;, two units above that.</p></div>
      <div class="appcard"><h4>Cafe, light cooking, hood up to 1.5 m</h4><p>1,200&ndash;2,200 m&sup3;/h at 200&ndash;300 Pa: one <strong>BXF-315</strong>, or two <strong>BXF-200</strong> in parallel if the duct route has several bends.</p></div>
      <div class="appcard"><h4>Restaurant hood run, 1.5&ndash;3 m</h4><p>3,000&ndash;4,500 m&sup3;/h at 250&ndash;400 Pa: <strong>two BXF-315 in parallel</strong> into a common plenum. One unit alone will not hold this duty.</p></div>
      <div class="appcard"><h4>Dishwash / pot wash</h4><p>Steam and humidity, 15&ndash;20 air changes: <strong>BXF-200</strong> or <strong>BXF-250</strong>, duct sloped back to a drain so condensate does not sit in the fan.</p></div>
      <div class="appcard"><h4>Prep room / dry store</h4><p>Heat and smell removal, 10&ndash;12 air changes: <strong>BXF-150</strong> or <strong>BXF-200</strong>, mounted at the opposite end of the room from the door.</p></div>
      <div class="appcard"><h4>Make-up air (supply side)</h4><p>85% of the extract volume, introduced away from the hood face: <strong>BXF-250</strong> or <strong>BXF-315</strong>, with a filter box on the intake.</p></div>
  </div>

  <span class="section-tag">SIZING</span>
  <h2 class="sec">Sizing a Kitchen Extract in Three Numbers</h2>
  <p style="max-width:900px;"><strong>1. Hood length.</strong> Allow 100 CFM per linear foot of hood face for light duty, 200 for medium (grills, fryers under a filter), 300 for heavy. That is roughly 0.5 m/s face velocity, the figure most hood manufacturers publish.</p>
  <p style="max-width:900px;"><strong>2. Convert and add margin.</strong> 1 CFM = 1.7 m&sup3;/h. Add 20% for the baffle filter, the elbows and the wall louvre &mdash; a fan rated at 2,200 m&sup3;/h free-air does not deliver 2,200 through a greasy filter and three bends.</p>
  <p style="max-width:900px;"><strong>3. Replace 85% of it.</strong> Make-up air is not optional: with the kitchen sealed, the extract fan starves, airflow drops by a third or more, the hood stops capturing, doors become hard to open and gas appliances can backdraft.</p>

  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:26px;margin:26px 0 44px;max-width:900px;">
    <h4 style="margin:0 0 10px;font-size:16px;">Worked example &mdash; 2.4 m (8 ft) medium-duty hood</h4>
    <p style="margin:0;">8 ft &times; 200 CFM = <strong>1,600 CFM = 2,715 m&sup3;/h</strong>. With the 20% allowance: <strong>3,260 m&sup3;/h</strong> at roughly 250&ndash;350 Pa. Two BXF-250 in parallel give 3,600 m&sup3;/h at 488 Pa &mdash; the smallest pairing that still meets the duty. Make-up air at 85%: <strong>2,770 m&sup3;/h</strong>, one BXF-315 plus one BXF-150, introduced low level on the far side of the room from the hood.</p>
  </div>

  <span class="section-tag">DUCT VELOCITY</span>
  <h2 class="sec">Duct Velocity: The Number Contractors Check</h2>
  <p style="max-width:900px;">Velocity is airflow divided by duct area, and it decides noise, pressure loss and whether grease keeps moving. For a grease duct, 7.6&ndash;10 m/s (1,500&ndash;2,000 fpm) keeps deposits from settling. For general exhaust, 5&ndash;8 m/s is comfortable. At rated airflow:</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>Model</th><th>Duct size (mm)</th><th>Rated airflow (m&sup3;/h)</th><th>Duct velocity (m/s)</th><th>Note</th></tr>
  <tr><td><strong>BXF-100</strong></td><td>&Phi;100</td><td>290</td><td>10.3</td><td>Short runs only &mdash; audible at this velocity</td></tr>
  <tr><td><strong>BXF-125</strong></td><td>&Phi;125</td><td>420</td><td>9.5</td><td>Inside the grease-duct band</td></tr>
  <tr><td><strong>BXF-150</strong></td><td>&Phi;150</td><td>620</td><td>9.8</td><td>Canteen and prep room extract</td></tr>
  <tr><td><strong>BXF-200</strong></td><td>&Phi;200</td><td>1,200</td><td>10.6</td><td>Upsize the duct one step on long runs</td></tr>
  <tr><td><strong>BXF-250</strong></td><td>&Phi;250</td><td>1,800</td><td>10.2</td><td>Best pressure of the small sizes</td></tr>
  <tr><td><strong>BXF-315</strong></td><td>&Phi;315</td><td>2,200</td><td>7.8</td><td>Sweet spot for kitchen duct runs</td></tr>
  </table>
  </div>
  <p class="tnote">Velocity at rated free-air airflow through a duct of the fan's own diameter. Every 100 mm step up in duct size drops velocity by roughly 40% and takes 10&ndash;20 dB(A) off the noise &mdash; if a run has to be quiet, use a larger duct and a reducer at the fan.</p>

  <span class="section-tag">PRESSURE</span>
  <h2 class="sec">Pressure Budget: What the Fan Actually Has to Beat</h2>
  <p style="max-width:900px;">Catalogue figures are free-air, at 0 Pa. A kitchen is never free-air. Add up the resistance before choosing the model:</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>Component</th><th>Typical pressure loss</th></tr>
  <tr><td>Stainless baffle grease filter</td><td>50&ndash;100 Pa (more as it loads)</td></tr>
  <tr><td>Wall louvre / outside hood</td><td>30&ndash;50 Pa</td></tr>
  <tr><td>Each 90&deg; elbow</td><td>15&ndash;25 Pa</td></tr>
  <tr><td>Straight duct, per metre</td><td>3&ndash;5 Pa</td></tr>
  <tr><td>Flexible connector, each</td><td>10 Pa</td></tr>
  </table>
  </div>
  <p class="tnote">Example: 6 m of duct (30 Pa) + 3 elbows (60 Pa) + filter (80 Pa) + louvre (40 Pa) = <strong>210 Pa</strong> on top of what the hood itself needs. Choose the model whose curve still gives your airflow at that pressure &mdash; on the BXF range that usually means BXF-200 and up. Send the run drawing and we will pick the model for you.</p>

  <span class="section-tag">MODEL RANGE</span>
  <h2 class="sec">The Six BXF Models</h2>
  <div class="twrap">
  <table class="spec-table">
  <tr><th rowspan="2">Model</th><th>Duct</th><th>Airflow</th><th>Airflow</th><th>Max static</th><th>Power</th><th>Noise</th><th>Pcs/ctn</th><th>CBM</th><th>G.W.</th></tr>
  <tr><th class="unit">(mm)</th><th class="unit">(m&sup3;/h)</th><th class="unit">(CFM)</th><th class="unit">(Pa)</th><th class="unit">(W)</th><th class="unit">(dB A)</th><th class="unit">(pcs)</th><th class="unit">(m&sup3;)</th><th class="unit">(kg/ctn)</th></tr>
  <tr><td><strong>BXF-100</strong></td><td>&Phi;100</td><td>290</td><td>171</td><td>150</td><td>48</td><td>28&ndash;31</td><td>6</td><td>0.101</td><td>11.20</td></tr>
  <tr><td><strong>BXF-125</strong></td><td>&Phi;125</td><td>420</td><td>247</td><td>180</td><td>50</td><td>28&ndash;31</td><td>6</td><td>0.101</td><td>12.70</td></tr>
  <tr><td><strong>BXF-150</strong></td><td>&Phi;150</td><td>620</td><td>365</td><td>300</td><td>60</td><td>28&ndash;32</td><td>6</td><td>0.119</td><td>15.45</td></tr>
  <tr><td><strong>BXF-200</strong></td><td>&Phi;200</td><td>1,200</td><td>706</td><td>380</td><td>120</td><td>45&ndash;50</td><td>4</td><td>0.097</td><td>14.00</td></tr>
  <tr><td><strong>BXF-250</strong></td><td>&Phi;250</td><td>1,800</td><td>1,060</td><td>488</td><td>200</td><td>54&ndash;60</td><td>1</td><td>0.043</td><td>7.35</td></tr>
  <tr><td><strong>BXF-315</strong></td><td>&Phi;315</td><td>2,200</td><td>1,295</td><td>693</td><td>330</td><td>60&ndash;70</td><td>1</td><td>0.072</td><td>9.15</td></tr>
  </table>
  </div>
  <p class="tnote">Rated at 220-240V / 50Hz, free inlet and free outlet. 60Hz versions for Saudi Arabia, UAE, Kuwait and Qatar, and 110V / 60Hz for North America, are produced to order. Net weight depends on winding and cable set &mdash; confirmed on the packing list per order.</p>

  <span class="section-tag">INSTALLATION</span>
  <h2 class="sec">Details That Decide Whether It Works</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Filter at the hood, fan at the discharge</h4><p>A stainless baffle filter in the canopy, then the fan downstream and outside the cooking space. Never inside the canopy, never in a grease duct run.</p></div>
      <div class="appcard"><h4>Leave access for cleaning</h4><p>Cleaning hatch before and after the fan. Even a filtered line coats the impeller over a season, and an unbalanced impeller is a warranty claim.</p></div>
      <div class="appcard"><h4>Flexible connectors both sides</h4><p>Two flexible sleeves and anti-vibration mounts if the fan hangs above a ceiling &mdash; this is what stops kitchen rumble reaching the dining room.</p></div>
      <div class="appcard"><h4>Slope the duct to drain</h4><p>Fall the run back towards the hood or a drain point so condensate and cleaning water do not collect inside the fan.</p></div>
      <div class="appcard"><h4>Isolator within sight</h4><p>Local isolator next to the fan for service. IP44 motor for washdown and dishwash extract areas.</p></div>
      <div class="appcard"><h4>Make-up air away from the hood</h4><p>Introduce low level on the opposite side of the room. Blowing supply across the hood face breaks capture and pushes grease into the room.</p></div>
  </div>

  <h2 class="sec">Certifications &amp; Factory</h2>
  <p style="max-width:900px;">CE is standard &mdash; certificate <strong>XH2601E0321945GC</strong> (Xihua International Testing &amp; Certification, Shenzhen), valid to 2031-01-28. The factory holds ISO 9001 (<strong>04625Q15304R1M</strong>) and CCC (<strong>2024010702612682</strong>). ETL can be arranged on request for US distribution; SAA for Australia is renewed per order and is not currently held. All numbers are published for you to verify on the <a href="/verify/" style="color:#C0392B;font-weight:700;text-decoration:none;">certificate verification page</a>.</p>
  <p style="max-width:900px;"><strong>Where they are made.</strong> Four workshops, 50,000 m&sup2; of production buildings, twelve injection machines and eight assembly lines in Shengzhou, Zhejiang &mdash; see the <a href="/baer-production-capacity" style="color:#C0392B;font-weight:700;text-decoration:none;">factory and capacity page</a>.</p>

  <span class="section-tag">BUYER FAQ</span>
  <h2 class="sec">Frequently Asked Questions</h2>
  <div class="faqwrap">
      <details><summary>Can I use a BXF duct fan for a restaurant hood? <span>+</span></summary><div class="fa">It depends on the grease load, and the honest answer is not always yes. For light cooking &mdash; electric hobs, ovens, warming equipment &mdash; with a stainless baffle filter at the hood and the fan mounted at the discharge end of the run, a BXF is a normal and cost-effective choice. For deep fryers, wok ranges and charbroilers the grease load is too high: that duct has to be welded and the fan has to be listed for grease service with the motor out of the airstream. The BXF motor sits in the airflow, so we will not recommend it there.</div></details>
      <details><summary>How much airflow does my kitchen need? <span>+</span></summary><div class="fa">Start from the hood: 100 CFM per linear foot of hood face for light duty, 200 for medium, 300 for heavy. Multiply by 1.7 for m&sup3;/h, then add 20% for the filter, elbows and wall louvre. A 2.4 m medium-duty hood works out at about 3,260 m&sup3;/h &mdash; two BXF-250 in parallel. Send the room and hood dimensions and we will run the numbers for you.</div></details>
      <details><summary>One fan or several in parallel? <span>+</span></summary><div class="fa">Parallel units are normal above about 2,500 m&sup3;/h. Two fans into a common plenum give redundancy &mdash; a kitchen can keep trading on one unit while the other is serviced &mdash; and the duct take-offs are easier to route than one large fan. Keep the branches symmetrical or the stronger fan will dominate the airflow.</div></details>
      <details><summary>Do I really need make-up air? <span>+</span></summary><div class="fa">Yes, about 85% of the extract volume. A sealed kitchen starves the extract fan: rated airflow can fall by a third, the hood stops capturing grease and steam, doors become hard to open, and gas appliances can backdraft carbon monoxide into the room. The supply must be introduced away from the hood face, ideally low level on the opposite wall.</div></details>
      <details><summary>Is it quiet enough next to a dining area? <span>+</span></summary><div class="fa">BXF-100 to 150 run at 28&ndash;32 dB(A), which is quieter than a normal conversation. The 200&ndash;315 sizes run 45&ndash;70 dB(A) and should not share a wall with seating. Three things fix noise: mount the fan outside the occupied space, fit flexible connectors, and use one duct size larger with a reducer at the fan.</div></details>
      <details><summary>Can you supply 60Hz or 110V versions? <span>+</span></summary><div class="fa">Yes. 220-240V / 50Hz is standard. 60Hz versions for Saudi Arabia, UAE, Kuwait, Qatar and Iraq, and 110V / 60Hz for the US and Canada, are built to order &mdash; state the voltage on the enquiry and it is included in the quote. 60Hz units run about 20% faster with proportionally more airflow, pressure and noise.</div></details>
      <details><summary>What is the minimum order and lead time? <span>+</span></summary><div class="fa">MOQ is 100 pcs per model for production orders; single units can be supplied as samples, charged at sample price with freight paid by the buyer. Bulk production runs 25&ndash;35 days from deposit and confirmed artwork. Packaging is neutral kraft carton by default, with printed colour cartons free above 1,000 pcs per model.</div></details>
      <details><summary>Do you supply the hood, filters and duct? <span>+</span></summary><div class="fa">No &mdash; we make the fans. Hoods, baffle filters and ductwork are supplied by your kitchen fabricator or local contractor, and we size the fan to their figures. If you send us the hood drawing and the duct route we will confirm the model, the pressure allowance and the duct velocity, and flag anything that will not work before you order.</div></details>
  </div>

  <div class="ctabox">
    <h2>Send the Hood Length and Duct Route</h2>
    <p>Tell us the hood length, the cooking equipment under it, the duct length and bends, the voltage and the destination port. We reply with the airflow you need, the model that delivers it at that pressure, and a formal quote &mdash; within 24 hours.</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">WhatsApp: +86 136 5585 9122</a>
      <a class="btn btn-red" href="/contact/">Send Inquiry</a>
      <a class="btn btn-ghost" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
    </div>
  </div>

</div>

'''

start = s.index('<section class="hero">')
end = s.index('<footer>')
s = s[:start] + BODY.replace('\n', '\r\n') + s[end:]

# ---------- strip inherited JSON-LD, rebuild ----------
s = re.sub(r'<script type="application/ld\+json">.*?</script>\r?\n?', '', s, flags=re.S)

faqs = [
 ("Can I use a BXF duct fan for a restaurant hood?",
  "It depends on the grease load. For light cooking (electric hobs, ovens, warming equipment) with a stainless baffle filter at the hood and the fan at the discharge end of the run, a BXF is a normal choice. For deep fryers, wok ranges and charbroilers the grease load is too high: the duct must be welded and the fan must be listed for grease service with the motor out of the airstream. The BXF motor sits in the airflow, so it is not recommended there."),
 ("How much airflow does my kitchen need?",
  "Allow 100 CFM per linear foot of hood face for light duty, 200 for medium and 300 for heavy, multiply by 1.7 for m3/h, then add 20% for the filter, elbows and wall louvre. A 2.4 m medium-duty hood works out at about 3,260 m3/h, which is two BXF-250 in parallel."),
 ("Do I need make-up air?",
  "Yes, about 85% of the extract volume. Without it the extract fan starves, rated airflow can drop by a third, the hood stops capturing, doors become hard to open and gas appliances can backdraft."),
 ("What duct velocity should a kitchen extract run at?",
  "7.6-10 m/s (1,500-2,000 fpm) for a grease duct to keep deposits moving, and 5-8 m/s for general exhaust. BXF-315 in a 315 mm duct runs at 7.8 m/s at rated airflow; the 100-250 mm sizes run at 9.5-10.6 m/s, which suits short runs."),
 ("Is it quiet enough next to a dining area?",
  "BXF-100 to 150 run at 28-32 dB(A), quieter than normal conversation. The 200-315 sizes run 45-70 dB(A). Mount the fan outside the occupied space, fit flexible connectors and use one duct size larger to cut noise."),
 ("Can you supply 60Hz or 110V versions?",
  "Yes. 220-240V/50Hz is standard; 60Hz versions for Saudi Arabia, UAE, Kuwait, Qatar and Iraq and 110V/60Hz for North America are built to order."),
 ("What is the minimum order and lead time?",
  "MOQ is 100 pcs per model for production orders. Samples are charged at sample price with freight paid by the buyer. Bulk production runs 25-35 days from deposit and confirmed artwork; packaging is neutral kraft carton by default with printed cartons free above 1,000 pcs per model."),
]

webpage = {"@context": "https://schema.org", "@graph": [{
    "@type": ["WebPage", "CollectionPage"],
    "@id": URL,
    "url": URL,
    "name": "Commercial Kitchen Exhaust Fans: Ducted Mixed-Flow Systems",
    "description": "Ducted mixed-flow kitchen exhaust fans from 290 to 2,200 m3/h and up to 693 Pa for cafe, restaurant, canteen and dishwash extract, with sizing by hood length, duct velocity and pressure budget.",
    "isPartOf": {"@id": "https://baer-ventilation.com/#website"},
    "inLanguage": "en",
    "dateModified": "2026-11-03",
    "breadcrumb": {"@id": URL + "#breadcrumb"}
}]}
crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://baer-ventilation.com/"},
    {"@type": "ListItem", "position": 2, "name": "Products", "item": "https://baer-ventilation.com/products/"},
    {"@type": "ListItem", "position": 3, "name": "Commercial Kitchen Exhaust Fans", "item": URL}]}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "@id": URL + "#faq",
       "mainEntity": [{"@type": "Question", "name": q,
                       "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

blocks = ''.join('<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + '</script>\r\n'
                 for b in (webpage, crumb, faq))
s = s.replace('</body>', blocks + '</body>')

io.open(DST, 'w', encoding='utf-8', newline='').write(s)

# ---------- validate ----------
t = io.open(DST, encoding='utf-8', newline='').read()
bad = 0
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    try:
        json.loads(b)
    except Exception as e:
        bad += 1
        print('JSON FAIL', e)
print('jsonld blocks:', len(re.findall(r'application/ld\+json', t)), 'invalid:', bad)
for tag in ['div', 'section', 'table', 'tr', 'td', 'th', 'p', 'details']:
    o = len(re.findall(r'<%s[\s>]' % tag, t)); c = t.count('</%s>' % tag)
    print(' ', tag, o, c, 'OK' if o == c else 'MISMATCH')
print('residual industrial refs:', t.count('industrial-exhaust-fans'))
print('residual 984:', t.count('984'))
raw = io.open(DST, 'rb').read()
print('CRLF', raw.count(b'\r\n'), 'bare LF', raw.count(b'\n') - raw.count(b'\r\n'))
import re as _re
_txt = _re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=_re.S)
_txt = _re.sub(r'<[^>]+>', ' ', _txt)
print('words:', len(_txt.split()))
