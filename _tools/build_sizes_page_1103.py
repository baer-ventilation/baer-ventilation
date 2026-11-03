# -*- coding: utf-8 -*-
"""Build /exhaust-fan-sizes-guide from the kitchen page shell."""
import io, re, json

SRC = 'commercial-kitchen-exhaust-fans.html'
DST = 'exhaust-fan-sizes-guide.html'
SLUG = 'exhaust-fan-sizes-guide'
URL = 'https://baer-ventilation.com/' + SLUG

TITLE = 'Exhaust Fan Sizes: 4, 6, 8, 10, 12 &amp; 18 Inch Explained | BAER'
DESC = ('What 4, 6, 8, 10, 12 and 18 inch exhaust fans actually deliver: airflow per size, room coverage, '
        'wall cut-out dimensions and why the same nominal size ranges from 150 to 1,670 m3/h.')

s = io.open(SRC, encoding='utf-8', newline='').read()

# ---------- head ----------
s = s.replace('<title>Commercial Kitchen Exhaust Fans &mdash; Ducted BXF Series | BAER</title>',
              '<title>' + TITLE + '</title>')
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="' + DESC + '">', s, count=1)
s = s.replace('<link rel="canonical" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">',
              '<link rel="canonical" href="' + URL + '">')
s = s.replace('<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">',
              '<link rel="alternate" hreflang="en" href="' + URL + '">')
s = s.replace('<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">',
              '<link rel="alternate" hreflang="x-default" href="' + URL + '">')
s = re.sub(r'<meta property="og:title" content="[^"]*">',
           '<meta property="og:title" content="' + TITLE + '">', s, count=1)
s = re.sub(r'<meta property="og:description" content="[^"]*">',
           '<meta property="og:description" content="Airflow, room coverage and wall cut-out for every size we make, '
           'from 4 inch bathroom fans to 18 inch panel fans. Size chart by room type and air changes.">', s, count=1)
s = re.sub(r'<meta property="og:url" content="[^"]*">',
           '<meta property="og:url" content="' + URL + '">', s, count=1)
s = re.sub(r'<meta name="twitter:title" content="[^"]*">',
           '<meta name="twitter:title" content="Exhaust Fan Sizes: 4 to 18 Inch Explained | BAER">', s, count=1)
s = re.sub(r'<meta name="twitter:description" content="[^"]*">',
           '<meta name="twitter:description" content="What each exhaust fan size really delivers, how to measure the '
           'opening, and the airflow a bathroom, kitchen or workshop needs.">', s, count=1)
s = s.replace('https://baer-ventilation.com/assets/images/Hf77c8f2216ff4576b9f83c896fdd000fq.webp',
              'https://baer-ventilation.com/assets/images/H42e66ea71d5445fcbb62c7c68e493d94v.webp')
s = s.replace('<meta property="og:image:alt" content="BXF mixed flow duct fan for commercial kitchen extract | BAER Ventilation">',
              '<meta property="og:image:alt" content="Exhaust fan size comparison: 4 to 18 inch models | BAER Ventilation">')
s = s.replace('<a href="/commercial-kitchen-exhaust-fans" class="active">EN</a>',
              '<a href="/exhaust-fan-sizes-guide" class="active">EN</a>')

# ---------- body ----------
BODY = u'''<section class="hero">
  <div class="hero-inner">
    <span class="hero-cat">Buyer Guide</span>
    <h1>Exhaust Fan Sizes: What 4, 6, 8, 10, 12 and 18 Inch Actually Deliver</h1>
    <p>The inch on the box is a <strong>mounting size</strong>, not a performance figure. In our own range a 6 inch fan moves anywhere from 150 to 1,670 m&sup3;/h depending on type &mdash; eleven times the airflow at the same nominal size. This page gives the airflow, room coverage and wall cut-out behind every size we make, so you order by the number that matters instead of the one on the carton.</p>
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
  <a href="/">Home</a> / <a href="/products/">Products</a> / <span>Exhaust Fan Sizes Guide</span>
</div>

<div class="container">

  <p style="font-size:16.5px;line-height:1.8;max-width:900px;margin-bottom:44px;">Two buyers order a &ldquo;6 inch exhaust fan&rdquo; and receive two completely different machines: one shifts 150 m&sup3;/h out of a bathroom, the other shifts 1,670 m&sup3;/h out of a workshop. Both are honestly described as 6 inch. This guide explains what the size refers to on each fan type, how much air each size can realistically move, and what hole you have to cut in the wall &mdash; the three things that decide whether the fan works in your space.</p>

  <span class="section-tag">THE BASICS</span>
  <h2 class="sec">The Inch Is a Mounting Size, Not an Airflow</h2>
  <p style="max-width:900px;">On a bathroom or panel fan, the inch refers to the nominal fan diameter inside a square wall panel &mdash; a 6 inch panel fan has a 200&times;200 mm faceplate. On a duct fan, the industry quotes the duct diameter in millimetres instead (100/125/150/200/250/315 mm). On a high-airflow wall shutter fan, the inch describes the blade and housing, and the same nominal size can be built with a much deeper blade and a faster motor. Airflow is set by blade design, motor speed and static pressure &mdash; never by the inch alone.</p>

  <div class="twrap">
  <table class="spec-table">
  <tr><th>Cheap-to-run guide</th><th>4&Prime; (100 mm)</th><th>6&Prime; (150 mm)</th><th>8&Prime; (200 mm)</th><th>10&Prime; (250 mm)</th><th>12&Prime; (300 mm)</th><th>18&Prime; (450 mm)</th></tr>
  <tr><td>Bathroom fan (quiet)</td><td>50&ndash;100 m&sup3;/h</td><td>100&ndash;220 m&sup3;/h</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
  <tr><td>Panel fan (KLT)</td><td>&mdash;</td><td>150 m&sup3;/h</td><td>380 m&sup3;/h</td><td>432 m&sup3;/h</td><td>792 m&sup3;/h</td><td>1,800 m&sup3;/h</td></tr>
  <tr><td>Duct fan (BXF)</td><td>290 m&sup3;/h</td><td>620 m&sup3;/h</td><td>1,200 m&sup3;/h</td><td>1,800 m&sup3;/h</td><td>2,200 m&sup3;/h (315 mm)</td><td>&mdash;</td></tr>
  <tr><td>High-airflow wall shutter</td><td>&mdash;</td><td>1,670 m&sup3;/h (984 CFM)</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td><td>&mdash;</td></tr>
  </table>
  </div>
  <p class="tnote">Rated free-air figures. Read the row, not the column: at 6 inch the spread is 150&ndash;1,670 m&sup3;/h, and the fan you need depends on the room, the mounting and the pressure &mdash; not on the nominal size.</p>

  <span class="section-tag">ROOM COVERAGE</span>
  <h2 class="sec">Which Size for Which Room</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Bathroom up to 5 m&sup2;</h4><p>About 10 m&sup3; of air at 8&ndash;10 changes per hour: <strong>80&ndash;100 m&sup3;/h</strong>. A 4 inch (100 mm) quiet bathroom fan is enough &mdash; going bigger mainly buys noise.</p></div>
      <div class="appcard"><h4>Bathroom 6&ndash;10 m&sup2;</h4><p><strong>150&ndash;200 m&sup3;/h</strong>. 6 inch bathroom fan, or a KLT-10B panel fan if the wall is masonry and you want a shutter louvre.</p></div>
      <div class="appcard"><h4>Kitchen 10&ndash;15 m&sup2; (domestic)</h4><p>12&ndash;15 air changes: <strong>400&ndash;550 m&sup3;/h</strong>. 8 inch panel fan (KLT-12B, 380 m&sup3;/h) as a minimum; use the ducted BXF-150 (620 m&sup3;/h) if the fan cannot sit on an outside wall.</p></div>
      <div class="appcard"><h4>Living room / bedroom 20&ndash;30 m&sup2;</h4><p>6&ndash;8 air changes: <strong>350&ndash;600 m&sup3;/h</strong>. 8 inch panel fan or a silent cabinet fan where noise matters more than volume.</p></div>
      <div class="appcard"><h4>Small office / shop 40&ndash;60 m&sup2;</h4><p><strong>650&ndash;900 m&sup3;/h</strong>. 12 inch panel fan (KLT-20B, 792 m&sup3;/h) or two smaller units on opposite walls.</p></div>
      <div class="appcard"><h4>Workshop / warehouse 60&ndash;100 m&sup2;</h4><p>8&ndash;12 air changes: <strong>1,800&ndash;3,000 m&sup3;/h</strong>. 18 inch panel fan (KLT-30B) or two 14 inch units (KLT-25B, 1,500 m&sup3;/h each).</p></div>
  </div>

  <span class="section-tag">THE CALCULATION</span>
  <h2 class="sec">Size by Air Changes, Not by Guesswork</h2>
  <p style="max-width:900px;">Every size decision reduces to one sum: <strong>room volume &times; air changes per hour = airflow needed</strong>. Volume is length &times; width &times; ceiling height, not floor area &mdash; the single most common mistake. Air change rates by room type:</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>Room</th><th>Air changes per hour</th><th>Notes</th></tr>
  <tr><td>Bathroom / WC</td><td>8&ndash;10</td><td>Higher if there is no window</td></tr>
  <tr><td>Domestic kitchen</td><td>12&ndash;15</td><td>15&ndash;20 if frying regularly</td></tr>
  <tr><td>Living room / bedroom</td><td>6&ndash;8</td><td>Comfort, not moisture control</td></tr>
  <tr><td>Office / shop</td><td>6&ndash;8</td><td>Add for occupancy above one person per 10 m&sup2;</td></tr>
  <tr><td>Workshop / warehouse</td><td>8&ndash;12</td><td>12&ndash;15 where there is welding or solvent</td></tr>
  <tr><td>Dishwash / laundry</td><td>15&ndash;20</td><td>Moisture-driven; use a ducted fan</td></tr>
  </table>
  </div>
  <p class="tnote">Worked example: a kitchen 4 &times; 3 m with a 2.9 m ceiling is 34.8 m&sup3;. At 15 air changes that is 522 m&sup3;/h &mdash; between the 8 inch panel fan (380) and the 6 inch duct fan (620). Take the larger of the two if the fan is ducted or the room has a window that stays shut. Conversions: 1 m&sup3;/h = 0.589 CFM; multiply m&sup3;/h by 0.59, or divide CFM by 0.59.</p>

  <span class="section-tag">MEASURING</span>
  <h2 class="sec">Measure the Opening, Not the Old Fan</h2>
  <p style="max-width:900px;">Three dimensions decide whether a replacement fits, and only one of them is the size printed on the box. The <strong>panel</strong> is the visible faceplate that covers the wall. The <strong>cut-out</strong> is the hole you actually make. The <strong>outlet</strong> is the spigot diameter, which matters if a duct connects to it.</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>Model</th><th>Nominal size</th><th>Panel (mm)</th><th>Wall cut-out (mm)</th><th>Outlet (&Phi; mm)</th><th>Airflow (m&sup3;/h)</th><th>Noise (dB)</th><th>Coverage</th></tr>
  <tr><td><a href="/product-klt-10b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-10B</a></td><td>6&Prime;</td><td>200&times;200</td><td>160&times;160</td><td>85</td><td>150</td><td>35</td><td>5&ndash;8 m&sup2;</td></tr>
  <tr><td><a href="/product-klt-12b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-12B</a></td><td>8&Prime;</td><td>250&times;250</td><td>205&times;205</td><td>100</td><td>380</td><td>38</td><td>12&ndash;15 m&sup2;</td></tr>
  <tr><td><a href="/product-klt-18b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-18B</a></td><td>10&Prime;</td><td>310&times;310</td><td>245&times;245</td><td>100</td><td>432</td><td>42</td><td>14&ndash;18 m&sup2;</td></tr>
  <tr><td><a href="/product-klt-20b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-20B</a></td><td>12&Prime;</td><td>340&times;340</td><td>290&times;290</td><td>100</td><td>792</td><td>45</td><td>26&ndash;32 m&sup2;</td></tr>
  <tr><td><a href="/product-klt-25b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-25B</a></td><td>14&Prime;</td><td>400&times;400</td><td>330&times;330</td><td>150</td><td>1,500</td><td>48</td><td>50&ndash;60 m&sup2;</td></tr>
  <tr><td><a href="/product-klt-30b" style="color:#C0392B;font-weight:700;text-decoration:none;">KLT-30B</a></td><td>18&Prime;</td><td>600&times;600</td><td>480&times;480</td><td>150</td><td>1,800</td><td>48</td><td>60&ndash;72 m&sup2;</td></tr>
  </table>
  </div>
  <p class="tnote">Coverage assumes a 2.7&ndash;3.0 m ceiling at 8&ndash;10 air changes. Note that the KLT-10B is called 6 inch but needs a 160&times;160 mm hole &mdash; the panel covers the rest. Send a photo of the opening with a tape measure across it and we will confirm the model before you cut anything.</p>

  <span class="section-tag">SAME SIZE, THREE FANS</span>
  <h2 class="sec">Why One 6 Inch Fan Moves 150 m&sup3;/h and Another 1,670</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Bathroom fan &mdash; 4&Prime; to 6&Prime;</h4><p>Quiet, low power, short duct. Built to shift 50&ndash;220 m&sup3;/h with an internal backdraught flap for a duct of 100&ndash;150 mm. The right choice when the limit is noise, not airflow.</p></div>
      <div class="appcard"><h4>Panel fan (KLT) &mdash; 6&Prime; to 18&Prime;</h4><p>Square wall fan with an automatic shutter louvre. Same nominal size, several times the airflow because the blade is deeper and the motor is bigger: 150 m&sup3;/h at 6 inch, 1,800 m&sup3;/h at 18 inch.</p></div>
      <div class="appcard"><h4>Duct fan (BXF) &mdash; 100 to 315 mm</h4><p>Mixed-flow impeller for pressure, not just volume: 290&ndash;2,200 m&sup3;/h and up to 693 Pa. Choose it when the fan sits away from the wall or the run has bends.</p></div>
      <div class="appcard"><h4>High-airflow wall shutter &mdash; one size, one job</h4><p>Our 6 inch industrial shutter fan is built for workshops: 984 CFM / 1,670 m&sup3;/h at up to 180 Pa. Same 6 inch label, industrial blade and motor.</p></div>
  </div>

  <span class="section-tag">RULES OF THUMB</span>
  <h2 class="sec">Five Things Buyers Get Wrong on Size</h2>
  <p style="max-width:900px;"><strong>1. Using floor area instead of volume.</strong> A 3 m ceiling holds 20% more air than a 2.5 m one. Multiply by height, always.</p>
  <p style="max-width:900px;"><strong>2. Buying one size up instead of fixing the duct.</strong> A fan with a long, narrow duct loses more airflow than the next size up would gain. 100 mm duct above 290 m&sup3;/h runs at 10 m/s and turns airflow into noise.</p>
  <p style="max-width:900px;"><strong>3. Forgetting make-up air.</strong> Every cubic metre out needs a way back in. A sealed room with a 1,000 m&sup3;/h fan can lose a third of that airflow and pull combustion gases down the flue.</p>
  <p style="max-width:900px;"><strong>4. Oversizing a bathroom.</strong> Above about 10 air changes you get a draught across the room, more noise, and a fan that pulls against the door seal. Match the size to the volume.</p>
  <p style="max-width:900px;"><strong>5. Ordering by inch across borders.</strong> A 6 inch fan is 150 mm in a duct, 200&times;200 mm on a panel and 152 mm on a US spec sheet. Quote both the inch size and the cut-out when you compare suppliers.</p>

  <span class="section-tag">RELATED</span>
  <h2 class="sec">Specifications &amp; Further Reading</h2>
  <div class="fgrid">
    <a class="fcard" href="/klt-series-panel-exhaust-fan"><h4>KLT Panel Series &mdash; All Six Sizes</h4></a>
    <a class="fcard" href="/product-inline-duct-fan"><h4>BXF Duct Fans &mdash; 100 to 315 mm</h4></a>
    <a class="fcard" href="/product-silent-bathroom-fan"><h4>Silent Bathroom Fans</h4></a>
    <a class="fcard" href="/product-window-fan"><h4>Window Exhaust Fans (no wall cutting)</h4></a>
    <a class="fcard" href="/bathroom-exhaust-fan-cfm-guide"><h4>Bathroom Airflow: How Much You Need</h4></a>
    <a class="fcard" href="/cfm-calculator"><h4>Airflow Calculator</h4></a>
    <a class="fcard" href="/commercial-kitchen-exhaust-fans"><h4>Commercial Kitchen Exhaust</h4></a>
    <a class="fcard" href="/industrial-exhaust-fans"><h4>Industrial Exhaust Fans</h4></a>
  </div>

  <h2 class="sec">Certifications &amp; Factory</h2>
  <p style="max-width:900px;">CE is standard &mdash; certificate <strong>XH2601E0321945GC</strong> (Xihua International Testing &amp; Certification, Shenzhen), valid to 2031-01-28. The factory holds ISO 9001 (<strong>04625Q15304R1M</strong>) and CCC (<strong>2024010702612682</strong>, covering KLT-10B to 18B at 220V/50Hz). ETL can be arranged on request; SAA is renewed per order. All numbers are published for you to verify on the <a href="/verify/" style="color:#C0392B;font-weight:700;text-decoration:none;">certificate verification page</a>.</p>

  <span class="section-tag">BUYER FAQ</span>
  <h2 class="sec">Frequently Asked Questions</h2>
  <div class="faqwrap">
      <details><summary>What size exhaust fan do I need for a 10 m&sup2; bathroom? <span>+</span></summary><div class="fa">A 10 m&sup2; bathroom with a 2.6 m ceiling holds 26 m&sup3;. At 8&ndash;10 air changes that is 210&ndash;260 m&sup3;/h, so a 6 inch (150 mm) bathroom fan rated around 220 m&sup3;/h. If there is no window, take the higher figure. A 4 inch fan is right for a small WC of 3&ndash;5 m&sup2;, not for a family bathroom.</div></details>
      <details><summary>Is a bigger fan always better? <span>+</span></summary><div class="fa">No. Oversizing causes a draught across the room, more noise, and in a sealed room it starves itself of make-up air so the extra capacity is never delivered. Size to the air-change rate and, where the load varies, use a two-speed or speed-controlled fan instead of a larger one.</div></details>
      <details><summary>My wall opening is 160&times;160 mm &mdash; which fan fits? <span>+</span></summary><div class="fa">That is the KLT-10B cut-out. Its 200&times;200 mm panel covers the opening and its 85 mm spigot takes a 100 mm duct &mdash; 150 m&sup3;/h, 35 dB. If you need more airflow through the same wall, keep the hole and use the BXF-100 duct fan in the run instead, at 290 m&sup3;/h.</div></details>
      <details><summary>Why is a 6 inch fan sometimes 150 m&sup3;/h and sometimes 1,670? <span>+</span></summary><div class="fa">Because the inch describes the mounting or blade diameter, not the motor or the blade depth. A 6 inch bathroom fan has a small backward-curved impeller and a low-power motor; our 6 inch industrial shutter fan has a deep axial blade and a much larger motor. Compare airflow at a stated static pressure, not the inch.</div></details>
      <details><summary>How do inches compare to the millimetres on duct fans? <span>+</span></summary><div class="fa">4&Prime; = 100 mm, 6&Prime; = 150 mm, 8&Prime; = 200 mm, 10&Prime; = 250 mm, 12&Prime; = 300 mm, 14&Prime; = 350 mm, 16&Prime; = 400 mm, 18&Prime; = 450 mm. Duct fans are quoted by duct diameter, so a 150 mm BXF is the &ldquo;6 inch&rdquo; one &mdash; but it delivers 620 m&sup3;/h, four times a 6 inch bathroom fan.</div></details>
      <details><summary>Can I fit a ducted fan if I only have a 100 mm hole? <span>+</span></summary><div class="fa">Yes &mdash; the BXF-100 is 290 m&sup3;/h at up to 150 Pa, but 100 mm duct runs at about 10 m/s at that airflow, so keep the run under 3&ndash;4 m with no more than two bends. Longer runs need a 150 mm duct and a reducer at the wall.</div></details>
      <details><summary>What if the wall cannot be cut at all? <span>+</span></summary><div class="fa">Use a window fan: the KLT-W window series covers 468&ndash;984 m&sup3;/h and mounts in the frame or a replacement glass panel, with the same shutter louvre. It is the usual answer for rented premises and heritage buildings.</div></details>
      <details><summary>Do sizes change for 60Hz or 110V? <span>+</span></summary><div class="fa">The physical size and cut-out stay the same; the airflow changes. A 60Hz motor runs about 20% faster, so the same fan moves proportionally more air and makes more noise. Quote the voltage with the size so the performance figures we send match what you will install.</div></details>
  </div>

  <div class="ctabox">
    <h2>Send the Room Size and the Opening</h2>
    <p>Tell us the room dimensions, the ceiling height, what the space is used for, and the wall or window opening you have. We reply with the airflow you need, the size and model that meets it, and a formal quote &mdash; within 24 hours.</p>
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

# ---------- JSON-LD ----------
s = re.sub(r'<script type="application/ld\+json">.*?</script>\r?\n?', '', s, flags=re.S)

faqs = [
 ("What size exhaust fan do I need for a 10 m2 bathroom?",
  "A 10 m2 bathroom with a 2.6 m ceiling holds 26 m3. At 8-10 air changes that is 210-260 m3/h, so a 6 inch (150 mm) bathroom fan rated around 220 m3/h. Without a window, take the higher figure. A 4 inch fan suits a 3-5 m2 WC, not a family bathroom."),
 ("Is a bigger exhaust fan always better?",
  "No. Oversizing causes draughts and noise, and in a sealed room the fan starves itself of make-up air so the extra capacity is never delivered. Size to the air-change rate and use a two-speed fan where the load varies."),
 ("My wall opening is 160x160 mm - which fan fits?",
  "That is the KLT-10B cut-out: 200x200 mm panel, 85 mm spigot for a 100 mm duct, 150 m3/h at 35 dB. If more airflow is needed through the same wall, keep the hole and use the BXF-100 duct fan in the run at 290 m3/h."),
 ("Why is a 6 inch fan sometimes 150 m3/h and sometimes 1,670 m3/h?",
  "The inch describes the mounting or blade diameter, not the motor or blade depth. A 6 inch bathroom fan has a small impeller and a low-power motor; a 6 inch industrial shutter fan has a deep axial blade and a much larger motor. Compare airflow at a stated static pressure."),
 ("How do inches compare with duct fan millimetres?",
  "4 inch = 100 mm, 6 = 150 mm, 8 = 200 mm, 10 = 250 mm, 12 = 300 mm, 14 = 350 mm, 16 = 400 mm, 18 = 450 mm. Duct fans are quoted by duct diameter, so a 150 mm BXF is the 6 inch one, delivering 620 m3/h - four times a 6 inch bathroom fan."),
 ("Can I fit a ducted fan with only a 100 mm hole?",
  "Yes - the BXF-100 gives 290 m3/h at up to 150 Pa, but 100 mm duct runs at about 10 m/s at that airflow, so keep the run under 3-4 m with at most two bends. Longer runs need 150 mm duct and a reducer at the wall."),
 ("What if the wall cannot be cut?",
  "Use a window fan. The KLT-W window series covers 468-984 m3/h and mounts in the frame or a replacement glass panel with the same shutter louvre."),
 ("Do sizes change for 60Hz or 110V?",
  "The physical size and cut-out stay the same; the airflow changes. A 60Hz motor runs about 20% faster, so the same fan moves more air and makes more noise. Quote the voltage with the size so the performance figures match the installation."),
]

webpage = {"@context": "https://schema.org", "@graph": [{
    "@type": ["WebPage", "Article"],
    "@id": URL,
    "url": URL,
    "headline": "Exhaust Fan Sizes: What 4, 6, 8, 10, 12 and 18 Inch Actually Deliver",
    "description": "Airflow, room coverage and wall cut-out dimensions for every exhaust fan size from 4 to 18 inch, with air-change sizing by room type.",
    "isPartOf": {"@id": "https://baer-ventilation.com/#website"},
    "inLanguage": "en",
    "dateModified": "2026-11-03",
    "author": {"@id": "https://baer-ventilation.com/#organization"},
    "publisher": {"@id": "https://baer-ventilation.com/#organization"},
    "breadcrumb": {"@id": URL + "#breadcrumb"}
}]}
crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": URL + "#breadcrumb", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://baer-ventilation.com/"},
    {"@type": "ListItem", "position": 2, "name": "Products", "item": "https://baer-ventilation.com/products/"},
    {"@type": "ListItem", "position": 3, "name": "Exhaust Fan Sizes Guide", "item": URL}]}
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
for tag in ['div', 'section', 'table', 'tr', 'td', 'th', 'p', 'details', 'a']:
    o = len(re.findall(r'<%s[\s>]' % tag, t)); c = t.count('</%s>' % tag)
    print(' ', tag, o, c, 'OK' if o == c else 'MISMATCH')
print('residual kitchen slug:', t.count('commercial-kitchen-exhaust-fans-'), t.count('Ducted BXF Series'))
raw = io.open(DST, 'rb').read()
print('CRLF', raw.count(b'\r\n'), 'bare LF', raw.count(b'\n') - raw.count(b'\r\n'))
_txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
_txt = re.sub(r'<[^>]+>', ' ', _txt)
print('words:', len(_txt.split()))
