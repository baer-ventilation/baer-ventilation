import io, re

SRC = 'product-6inch-984cfm.html'
DST = 'industrial-exhaust-fans.html'

s = io.open(SRC, encoding='utf-8', newline='').read()

# ---------- 1. head 重写 ----------
s = s.replace(
 '<title>6 Inch 984 CFM Wall Shutter Exhaust Fan Manufacturer | BAER</title>',
 '<title>Industrial Exhaust Fans for Warehouses &amp; Workshops | BAER</title>')

def repl_meta(s, pattern, new):
    return re.sub(pattern, new, s, count=1)

# description
s = re.sub(r'<meta name="description" content="[^"]*">',
 '<meta name="description" content="Factory-direct industrial exhaust fans from 984 to 4,500 CFM for warehouses, workshops and loading areas. Wall shutter, axial and ducted types, CE certified, 50Hz or 60Hz.">', s, count=1)

# canonical + hreflang
s = s.replace('<link rel="canonical" href="https://baer-ventilation.com/product-6inch-984cfm">',
              '<link rel="canonical" href="https://baer-ventilation.com/industrial-exhaust-fans">')
s = re.sub(r'<link rel="alternate" hreflang="[a-z-]+" href="https://baer-ventilation.com/(ar/|zh/)?product-6inch-984cfm">\r?\n?', '', s)
s = s.replace('<link rel="canonical" href="https://baer-ventilation.com/industrial-exhaust-fans">',
 '<link rel="canonical" href="https://baer-ventilation.com/industrial-exhaust-fans">\r\n'
 '<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/industrial-exhaust-fans">\r\n'
 '<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/industrial-exhaust-fans">')

# og
s = re.sub(r'<meta property="og:title" content="[^"]*">',
 '<meta property="og:title" content="Industrial Exhaust Fans for Warehouses &amp; Workshops | BAER">', s, count=1)
s = re.sub(r'<meta property="og:description" content="[^"]*">',
 '<meta property="og:description" content="Wall shutter, axial and ducted exhaust fans from 984 to 4,500 CFM for warehouses, workshops and loading areas. Factory-direct, CE certified.">', s, count=1)
s = re.sub(r'<meta property="og:url" content="[^"]*">',
 '<meta property="og:url" content="https://baer-ventilation.com/industrial-exhaust-fans">', s, count=1)
s = s.replace('<meta property="og:type" content="product">', '<meta property="og:type" content="website">')

# 语言切换：新页暂无 ar/zh
s = s.replace('<a href="/product-6inch-984cfm" class="active">EN</a>\r\n      <a href="/zh/product-6inch-984cfm">中文</a>\r\n      <a href="/ar/product-6inch-984cfm">العربية</a>',
              '<a href="/industrial-exhaust-fans" class="active">EN</a>')

# ---------- 2. body 重写 ----------
start = s.index('<section class="hero">')
end = s.index('<footer>')

BODY = '''<section class="hero">
  <div class="hero-inner">
    <span class="hero-cat">Industrial Ventilation</span>
    <h1>Industrial Exhaust Fans for Warehouses, Workshops and Factories</h1>
    <p>Wall shutter, axial and ducted exhaust fans from <strong>984 to 4,500 CFM</strong>, built for continuous duty on production floors, storage halls and loading areas. CE certified, 220-240V/50Hz or 110V/60Hz, shipped factory-direct from Zhejiang.</p>
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
  <a href="/">Home</a> / <a href="/products/">Products</a> / <span>Industrial Exhaust Fans</span>
</div>

<div class="container">

  <p style="font-size:16.5px;line-height:1.8;max-width:900px;margin-bottom:44px;">Industrial exhaust fans do one job: move hot air, fumes and dust out of a building fast enough that people can work and goods do not spoil. Choosing one is not about brand &mdash; it is about matching airflow and mounting to the space. This page explains which of our four fan families fits which industrial space, how to calculate the airflow you need, and what to send us to get an exact quote in 24 hours.</p>

  <h2 class="sec">Which Fan Fits Which Job</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Production floor / workshop</h4><p>Removes welding fume, heat and airborne dust. Wall shutter fans 8&Prime;&ndash;12&Prime; mounted high on the external wall, opposite the fresh-air inlet.</p></div>
      <div class="appcard"><h4>Warehouse &amp; storage hall</h4><p>Stops condensation on stored goods and clears stale air. KLT panel exhaust fans 20B&ndash;30B, or large shutter fans for high bays.</p></div>
      <div class="appcard"><h4>Loading dock / dispatch</h4><p>Clears vehicle exhaust during loading. Wall shutter fans 12&Prime; or KLT-30B, interlocked with the dock door where possible.</p></div>
      <div class="appcard"><h4>Packing &amp; assembly line</h4><p>Operator comfort rather than process extraction. 6&Prime;&ndash;8&Prime; shutter fans or KLT-10B&ndash;18B at regular intervals.</p></div>
      <div class="appcard"><h4>Control room / workshop office</h4><p>Quiet, low-vibration air change next to the plant floor. Silent cabinet fans ducted to the outside.</p></div>
      <div class="appcard"><h4>Ducted run to an outside wall</h4><p>When the fan cannot sit on the wall itself. BXF mixed-flow duct fans, 100&ndash;315 mm, for runs up to several metres.</p></div>
  </div>

  <span class="section-tag">SIZING</span>
  <h2 class="sec">How Much Airflow You Actually Need</h2>
  <p style="max-width:900px;margin-bottom:20px;">Industrial ventilation is sized by <strong>air changes per hour (ACH)</strong>: the building volume multiplied by how many times the air should be replaced each hour. Typical design values by space:</p>
  <table class="ptable" style="max-width:900px;margin-bottom:22px;">
    <tr><th>Space type</th><th>Typical air changes per hour</th><th>Notes</th></tr>
    <tr><td>General warehouse / storage</td><td>6 &ndash; 8 ACH</td><td>Raise it if goods are moisture-sensitive</td></tr>
    <tr><td>Assembly / packing workshop</td><td>8 &ndash; 12 ACH</td><td>Occupant comfort driven</td></tr>
    <tr><td>Welding / fabrication bay</td><td>12 &ndash; 15 ACH</td><td>Local extraction still recommended at the arc</td></tr>
    <tr><td>Loading dock / vehicle area</td><td>10 &ndash; 15 ACH</td><td>Higher during peak dispatch hours</td></tr>
    <tr><td>Storage with condensation risk</td><td>4 &ndash; 6 ACH</td><td>Combine with dehumidification in humid climates</td></tr>
  </table>
  <p style="max-width:900px;margin-bottom:14px;"><strong>Worked example.</strong> A hall of 20 m &times; 10 m &times; 5 m = 1,000 m&sup3; used as a workshop at 10 ACH needs 10,000 m&sup3;/h, which is about 5,900 CFM. That is six 6&Prime; units at 984 CFM each, or two larger 12&Prime; units &mdash; the choice depends on how many wall openings you have.</p>
  <p style="max-width:900px;margin-bottom:44px;font-size:14px;color:#64748B;">These are design starting points, not a substitute for your HVAC engineer&rsquo;s calculation. Send us the building dimensions and we will size it with you &mdash; or use the <a href="/cfm-calculator" style="color:#C0392B;font-weight:700;text-decoration:none;">CFM calculator</a> and read the longer <a href="/exhaust-fan-airflow-calculation-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">airflow calculation guide</a>.</p>

  <span class="section-tag">PRODUCT RANGE</span>
  <h2 class="sec">Four Families, One Factory</h2>
  <div class="appgrid">
      <div class="appcard"><h4>Wall shutter series, 6&Prime;&ndash;12&Prime;</h4><p>984 CFM at 6&Prime; rising to about 4,500 CFM at 12&Prime;. Automatic back-draft shutter, continuous-duty motor, up to 180 Pa. <a href="/product-6inch-984cfm" style="color:#C0392B;font-weight:700;text-decoration:none;">See the 6&Prime; specification &rarr;</a></p></div>
      <div class="appcard"><h4>KLT panel exhaust, 10B&ndash;30B</h4><p>150&ndash;1,800 m&sup3;/h in six sizes. The volume workhorse for walls and windows, built around a pressed-steel panel and louvre shutter. <a href="/klt-series-panel-exhaust-fan" style="color:#C0392B;font-weight:700;text-decoration:none;">Full KLT specification &rarr;</a></p></div>
      <div class="appcard"><h4>BXF mixed-flow duct fans</h4><p>100&ndash;315 mm duct sizes for runs where the fan sits inside the duct line rather than on the wall. <a href="/product-inline-duct-fan" style="color:#C0392B;font-weight:700;text-decoration:none;">Inline duct fan page &rarr;</a></p></div>
      <div class="appcard"><h4>Silent cabinet fans</h4><p>Acoustic enclosure for control rooms, offices and areas where noise is the constraint. <a href="/product-silent-cabinet-fan" style="color:#C0392B;font-weight:700;text-decoration:none;">Cabinet fan page &rarr;</a></p></div>
      <div class="appcard"><h4>Axial fans FA8-20 to FA16-40</h4><p>8&Prime;&ndash;16&Prime; axial impellers for high-volume, low-pressure duty &mdash; circulation and general dilution. <a href="/products/" style="color:#C0392B;font-weight:700;text-decoration:none;">See product list &rarr;</a></p></div>
      <div class="appcard"><h4>OEM &amp; private label</h4><p>Your brand on the housing and carton, from 500 pcs per model. <a href="/oem-private-label-exhaust-fan-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">How OEM works &rarr;</a></p></div>
  </div>

  <span class="section-tag">SPECIFICATION</span>
  <h2 class="sec">What the Wall Shutter Series Delivers</h2>
  <div class="pwrap">
    <div class="pimg"><img src="/assets/images/H42e66ea71d5445fcbb62c7c68e493d94v.webp" alt="BAER industrial wall shutter exhaust fan for warehouse ventilation" loading="lazy" decoding="async" width="600" height="600"></div>
    <div class="pinfo">
      <h3>Key Specifications</h3>
      <table class="ptable">
      <tr><th>Fan diameter</th><td>6&Prime; (150 mm) &mdash; 8&Prime; / 10&Prime; / 12&Prime; available</td></tr>
      <tr><th>Airflow</th><td>984 CFM / 1,670 m&sup3;/h at 6&Prime;; up to about 4,500 CFM at 12&Prime;</td></tr>
      <tr><th>Static pressure</th><td>Up to 180 Pa at 6&Prime; (model dependent)</td></tr>
      <tr><th>Power</th><td>80 &ndash; 150 W (6&Prime;); higher on larger sizes</td></tr>
      <tr><th>Voltage</th><td>220-240V / 50Hz standard; 110V / 60Hz and 60Hz Gulf versions available</td></tr>
      <tr><th>Noise</th><td>&le; 62 dB(A) at 6&Prime;</td></tr>
      <tr><th>Shutter</th><td>Automatic back-draft louvre &mdash; closes when the fan stops</td></tr>
      <tr><th>Duty</th><td>Continuous operation; every unit test-run before packing</td></tr>
      <tr><th>Certification</th><td>CE (ISO 9001, CCC and CB for the factory)</td></tr>
      <tr><th>Price</th><td>On request &mdash; formal quote within 24 hours</td></tr>
      </table>
      <p style="font-size:12.5px;color:#64748B;margin:10px 0 0;">Pricing depends on size, voltage and quantity. Send your target airflow, voltage and destination port &mdash; exact quote within 24 hours.</p>
    </div>
  </div>

  <div class="certstrip">
    <div class="ct ce">CE<small>XH2601E0321945GC</small></div>
    <div class="ct">ISO 9001<small>04625Q15304R1M</small></div>
    <div class="ct">CCC<small>2024010702612682</small></div>
    <div class="ct">CB<small>report on file</small></div>
    <div class="ct">ETL<small>on request</small></div>
  </div>
  <p style="max-width:900px;margin:-40px 0 44px;font-size:14px;color:#64748B;">Certificate numbers are published so you can verify them independently &mdash; check them on the <a href="/verify/" style="color:#C0392B;font-weight:700;text-decoration:none;">verification page</a> or read the <a href="/exhaust-fan-certifications-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">certification guide</a>.</p>

  <span class="section-tag">BEFORE YOU ORDER</span>
  <h2 class="sec">What Industrial Buyers Ask Us First</h2>
  <p style="max-width:900px;margin-bottom:16px;"><strong>MOQ and lead time.</strong> Stock models: 100 pcs, shipping from inventory. OEM with your branding: 500 pcs per model, bulk production 25&ndash;35 days from deposit and confirmed artwork. The <a href="/exhaust-fan-moq-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">MOQ guide</a> explains why the two thresholds differ.</p>
  <p style="max-width:900px;margin-bottom:16px;"><strong>Voltage for your market.</strong> Standard is 220-240V/50Hz. 110V/60Hz for North America and 60Hz versions for the Gulf are built to order &mdash; see the <a href="/exhaust-fan-60hz-gulf-voltage" style="color:#C0392B;font-weight:700;text-decoration:none;">60Hz Gulf voltage page</a> for detail.</p>
  <p style="max-width:900px;margin-bottom:16px;"><strong>How many fit in a container.</strong> Sizes and carton volumes vary enough that this changes your landed cost. The <a href="/exhaust-fan-container-loading-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">container loading guide</a> has per-model figures for 20GP, 40GP and 40HQ.</p>
  <p style="max-width:900px;margin-bottom:44px;"><strong>Where they are made.</strong> Four workshops, 50,000 m&sup2; of production buildings, twelve injection machines and eight assembly lines in Shengzhou, Zhejiang &mdash; see the <a href="/baer-production-capacity" style="color:#C0392B;font-weight:700;text-decoration:none;">factory and capacity page</a>.</p>

  <span class="section-tag">BUYER FAQ</span>
  <h2 class="sec">Frequently Asked Questions</h2>
  <div class="faqwrap">
      <details><summary>What size exhaust fan do I need for a 1,000 m&sup3; warehouse? <span>+</span></summary><div class="fa">At 6&ndash;8 air changes per hour a 1,000 m&sup3; store needs 6,000&ndash;8,000 m&sup3;/h, roughly 3,500&ndash;4,700 CFM. That is four to five 6&Prime; wall shutter fans, or two 12&Prime; units. Send the room dimensions and we will confirm the count.</div></details>
      <details><summary>Can you supply 60Hz or 110V versions? <span>+</span></summary><div class="fa">Yes. 220-240V/50Hz is standard. 110V/60Hz for the US and Canada, and 60Hz versions for Saudi Arabia, UAE, Kuwait, Qatar and Iraq, are produced to order. State the voltage on the enquiry and it is built into the quote.</div></details>
      <details><summary>Does the shutter stop air coming back in? <span>+</span></summary><div class="fa">The automatic back-draft louvre closes when the fan stops, which stops outside air, rain and dust entering through the opening. It is not a sealed damper &mdash; for a fully airtight line you need a separate motorised damper.</div></details>
      <details><summary>Is the motor rated for continuous running? <span>+</span></summary><div class="fa">Yes. These are continuous-duty motors, and every unit is test-run on the line before packing. For dust-heavy or high-temperature environments tell us the condition so the winding class and insulation can be matched.</div></details>
      <details><summary>Can the fan be mounted with ducting instead of on the wall? <span>+</span></summary><div class="fa">A wall shutter fan is designed for direct wall or window mounting. If the fan has to sit away from the wall, use the BXF mixed-flow duct fan instead &mdash; it is built for duct runs of several metres and comes in 100&ndash;315 mm sizes.</div></details>
      <details><summary>What certifications come with the fan? <span>+</span></summary><div class="fa">CE is standard. The factory holds ISO 9001, CCC and CB, with certificate numbers published on this page. ETL can be arranged on request for US distribution. SAA for Australia is renewed per order &mdash; it is not currently held.</div></details>
      <details><summary>Do you supply spare parts and motors? <span>+</span></summary><div class="fa">Yes, motors, blades and shutter assemblies can be shipped with a production order so you hold stock locally. Ask for a parts list with your quote.</div></details>
  </div>

  <div class="ctabox">
    <h2>Send Your Room Size, Get a Sized Recommendation</h2>
    <p>Tell us the building dimensions, the process inside, the voltage and the destination port. We reply with the airflow you need, the models that meet it and a formal quote &mdash; within 24 hours.</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">WhatsApp: +86 136 5585 9122</a>
      <a class="btn btn-red" href="/contact/">Send Inquiry</a>
      <a class="btn btn-ghost" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
    </div>
  </div>

</div>

'''

s = s[:start] + BODY + s[end:]

# ---------- 3. 追加结构化数据（Breadcrumb + FAQPage） ----------
import json
faqs = [
 ("What size exhaust fan do I need for a 1,000 m3 warehouse?",
  "At 6-8 air changes per hour a 1,000 m3 store needs 6,000-8,000 m3/h, roughly 3,500-4,700 CFM. That is four to five 6 inch wall shutter fans, or two 12 inch units. Send the room dimensions and we will confirm the count."),
 ("Can you supply 60Hz or 110V versions?",
  "Yes. 220-240V/50Hz is standard. 110V/60Hz for the US and Canada, and 60Hz versions for Saudi Arabia, UAE, Kuwait, Qatar and Iraq, are produced to order. State the voltage on the enquiry and it is built into the quote."),
 ("Does the shutter stop air coming back in?",
  "The automatic back-draft louvre closes when the fan stops, which stops outside air, rain and dust entering through the opening. It is not a sealed damper - for a fully airtight line you need a separate motorised damper."),
 ("Is the motor rated for continuous running?",
  "Yes. These are continuous-duty motors, and every unit is test-run on the line before packing. For dust-heavy or high-temperature environments tell us the condition so the winding class and insulation can be matched."),
 ("Can the fan be mounted with ducting instead of on the wall?",
  "A wall shutter fan is designed for direct wall or window mounting. If the fan has to sit away from the wall, use the BXF mixed-flow duct fan instead - it is built for duct runs of several metres and comes in 100-315 mm sizes."),
 ("What certifications come with the fan?",
  "CE is standard. The factory holds ISO 9001, CCC and CB, with certificate numbers published on this page. ETL can be arranged on request for US distribution. SAA for Australia is renewed per order - it is not currently held."),
 ("Do you supply spare parts and motors?",
  "Yes, motors, blades and shutter assemblies can be shipped with a production order so you hold stock locally. Ask for a parts list with your quote."),
]
ld_faq = {
 "@context":"https://schema.org","@type":"FAQPage",
 "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
}
ld_crumb = {
 "@context":"https://schema.org","@type":"BreadcrumbList",
 "itemListElement":[
   {"@type":"ListItem","position":1,"name":"Home","item":"https://baer-ventilation.com/"},
   {"@type":"ListItem","position":2,"name":"Products","item":"https://baer-ventilation.com/products/"},
   {"@type":"ListItem","position":3,"name":"Industrial Exhaust Fans","item":"https://baer-ventilation.com/industrial-exhaust-fans"}
 ]
}
block = ('<script type="application/ld+json">' + json.dumps(ld_faq, ensure_ascii=False) + '</script>\r\n'
         '<script type="application/ld+json">' + json.dumps(ld_crumb, ensure_ascii=False) + '</script>\r\n')
s = s.replace('</body>', block + '</body>')

# ---------- 4. 统一 CRLF 并写盘 ----------
s = s.replace('\r\n','\n').replace('\n','\r\n')
io.open(DST,'w',encoding='utf-8',newline='').write(s)

b = io.open(DST,'rb').read()
print('written', DST, len(b), 'bytes')
print('CRLF', b.count(b'\r\n'), 'bare LF', b.count(b'\n')-b.count(b'\r\n'))
t = io.open(DST,encoding='utf-8').read()
for tag in ['title','h1','table','tr','td','th','div','details','section','p']:
    o=len(re.findall(r'<%s[\s>]'%tag,t)); c=t.count('</%s>'%tag)
    print(f'  {tag}: {o}/{c}', 'OK' if o==c else 'MISMATCH')
print('canonical:', re.search(r'<link rel="canonical" href="([^"]+)"',t).group(1))
print('hreflang count:', t.count('hreflang='))
print('残留 product-6inch 链接（应仅内链）:', t.count('/product-6inch-984cfm'))
