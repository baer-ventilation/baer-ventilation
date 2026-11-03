# -*- coding: utf-8 -*-
"""Build /exhaust-fan-maintenance-guide from the sizes-guide shell (head/nav/footer reused verbatim)."""
import re, io

SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"
SLUG = "exhaust-fan-maintenance-guide"
URL = "https://baer-ventilation.com/" + SLUG

shell = open(SITE + "exhaust-fan-sizes-guide.html", "rb").read().decode("utf-8")

TITLE = "Exhaust Fan Maintenance: 12-Month Schedule &amp; Failures | BAER"
DESC = ("A 12-month maintenance schedule for wall, panel and duct exhaust fans: what fails first, how to clean each "
        "type, spare parts to keep, and when repair stops paying.")
H1 = "Exhaust Fan Maintenance: What Fails First, and What to Do Each Quarter"

META = f"""<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<link rel="alternate" hreflang="en" href="{URL}">
<link rel="alternate" hreflang="x-default" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="BAER Ventilation">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="Exhaust Fan Maintenance: 12-Month Schedule and Failure Points">
<meta property="og:description" content="What actually fails on an exhaust fan, the cleaning interval each installation needs, and the spare parts worth keeping on site.">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="https://baer-ventilation.com/assets/images/H42e66ea71d5445fcbb62c7c68e493d94v.webp">
<meta property="og:image:alt" content="Exhaust fan maintenance schedule and service points | BAER Ventilation">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Exhaust Fan Maintenance: What Fails First">
<meta name="twitter:description" content="A 12-month schedule for wall, panel and duct fans, the checks that catch a failing unit early, and the spares worth keeping.">
<meta name="twitter:image" content="https://baer-ventilation.com/assets/images/H42e66ea71d5445fcbb62c7c68e493d94v.webp">
"""

# ---------- head ----------
head_end = shell.find("</head>")
head = shell[:head_end]
t_i = head.find("<title>")
theme_i = head.find('<meta name="theme-color"')
head = head[:t_i] + META + head[theme_i:]

# ---------- body prefix (topbar + nav) ----------
hero_i = shell.find('<section class="hero">')
prefix = shell[head_end:hero_i]
prefix = prefix.replace('<a href="/exhaust-fan-sizes-guide" class="active">EN</a>',
                        f'<a href="/{SLUG}" class="active">EN</a>')
assert f'/{SLUG}" class="active"' in prefix, "lang-switch not replaced"

HERO = f"""<section class="hero">
  <div class="hero-inner">
    <span class="hero-cat">Service Guide</span>
    <h1>{H1}</h1>
    <p>Most exhaust fans replaced under complaint are not burnt out &mdash; they are dusty, loose, or running on a dead capacitor. A fan that is cleaned and checked on a schedule runs its rated airflow for years; one that is ignored loses 15&ndash;30% of it in a dusty workshop inside two seasons. This guide sets out what fails first, what to check each quarter, and the spares worth keeping on site.</p>
    <p style="font-size:13px;color:#64748B;margin:10px 0 0;">Last updated: November 3, 2026</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        WhatsApp Inquiry
      </a>
      <a class="btn btn-red" href="/contact/">Ask About Spares</a>
      <a class="btn btn-ghost" href="/faq">Site FAQ</a>
    </div>
  </div>
</section>
"""

CRUMB = f"""<div class="crumb">
  <a href="/">Home</a> / <a href="/products/">Products</a> / <span>Exhaust Fan Maintenance</span>
</div>
"""

BODY = """
  <p style="font-size:16.5px;line-height:1.8;max-width:900px;margin-bottom:44px;">A fan is one of the few things on a building that can be judged before it fails. Dust on the blade, a shutter flap that no longer closes flat, a motor that hums a second before it spins &mdash; each one is visible or audible months before the unit stops. This page is the schedule we give to buyers who maintain their own installations, and the same list our own service team works from.</p>

  <span class="section-tag">FAILURE ORDER</span>
  <h2 class="sec">What Fails First, Second and Third</h2>
  <p style="max-width:900px;">Airflow loss and motor failure are usually the last two things to happen, not the first. In the warranty claims and spare-parts requests we handle, the order below is consistent across wall, panel and duct fans &mdash; and the first three items account for most of them.</p>

  <div class="twrap">
  <table class="spec-table">
  <tr><th>Order</th><th>What fails</th><th>How you notice it</th><th>Typical trigger</th><th>Repair</th></tr>
  <tr><td>1</td><td>Run capacitor</td><td>Fan hums but does not spin; needs a nudge; spins slowly</td><td>Heat and age; a capacitor is a wear item with a shorter life than the motor</td><td>Replace capacitor &mdash; 10 minute job, lowest-cost repair on the whole fan</td></tr>
  <tr><td>2</td><td>Blade fouling and imbalance</td><td>New vibration, rumble, or a fan that got noticeably quieter (because it is moving less air)</td><td>Dust, lint, grease or pollen building unevenly on one side of the blade</td><td>Clean and rebalance; check the shaft for play while the blade is off</td></tr>
  <tr><td>3</td><td>Shutter mechanism</td><td>Flaps stay half open when off, rattle in wind, or stick when the fan starts</td><td>Dust in the rails, a bent flap pin, a stretched spring, or grease that has collected grit</td><td>Clean rails, straighten pins, replace the flap set; lubricate dry, never with grease</td></tr>
  <tr><td>4</td><td>Bearings</td><td>Rumble that grows over weeks, or a grinding note at start-up</td><td>Dust ingestion and long idle periods; sealed bearings cannot be re-greased</td><td>Replace motor or bearing set &mdash; usually not economic on small panel fans</td></tr>
  <tr><td>5</td><td>Motor winding</td><td>Trips the breaker, smells hot, or will not start at all</td><td>Almost always the consequence of a seized bearing or a blocked blade run for hours</td><td>Replace motor; find the cause first or the new one fails the same way</td></tr>
  </table>
  </div>
  <p class="tnote">Capacitor values differ by motor size: typically 1.0&ndash;2.0 &micro;F on 100&ndash;150 mm fans, 2.0&ndash;3.5 &micro;F on 200&ndash;250 mm and 4.0&ndash;8.0 &micro;F on 300&ndash;450 mm. Always read the value printed on the old capacitor or the motor nameplate before ordering a replacement.</p>

  <span class="section-tag">SCHEDULE</span>
  <h2 class="sec">The 12-Month Schedule, by Environment</h2>
  <p style="max-width:900px;">The interval is set by what the air carries, not by the fan. A bathroom fan in a house and a shutter fan on a welding bay are the same maintenance task at completely different frequencies.</p>

  <div class="twrap">
  <table class="spec-table">
  <tr><th>Installation</th><th>Clean blade and grille</th><th>Shutter / damper check</th><th>Electrical check</th><th>Full service</th></tr>
  <tr><td>Home bathroom, kitchen, living space</td><td>Every 6 months</td><td>Every 12 months</td><td>Every 24 months</td><td>Every 24 months</td></tr>
  <tr><td>Office, shop, clinic (light dust)</td><td>Every 3&ndash;6 months</td><td>Every 6 months</td><td>Every 12 months</td><td>Every 12 months</td></tr>
  <tr><td>Workshop, warehouse, welding, woodworking</td><td>Every 1&ndash;3 months</td><td>Every 3 months</td><td>Every 6 months</td><td>Every 6&ndash;12 months</td></tr>
  <tr><td>Commercial kitchen extraction</td><td>Every 1&ndash;3 months (grease)</td><td>Every month</td><td>Every 6 months</td><td>Every 6 months, plus duct clean per fire code</td></tr>
  <tr><td>Coastal or high-humidity site</td><td>Every 3 months</td><td>Every 3 months</td><td>Every 6 months (insulation test)</td><td>Every 12 months</td></tr>
  <tr><td>Seasonal / long idle</td><td>Before and after the season</td><td>Before the season</td><td>Before the season</td><td>Run 10 minutes every month while idle</td></tr>
  </table>
  </div>
  <p class="tnote">Intervals assume continuous daytime operation. For 24-hour duty, halve the cleaning interval. Where the fan runs against a filter, clean the filter more often than the fan &mdash; a loaded filter is what pushes the fan down its curve.</p>

  <span class="section-tag">HOW TO CLEAN</span>
  <h2 class="sec">Cleaning Each Fan Family Without Damaging It</h2>
  <p style="max-width:900px;">The single most common cleaning mistake is water in the motor. Everything else is recoverable; a wet winding is not. Isolate the fan at the breaker before any of the steps below, and do not rely on the wall switch alone.</p>

  <div class="appgrid">
    <div class="appcard"><h4>Panel fan (KLT series)</h4><p>Release the front grille, lift the blade off the shaft, wash the blade and grille in warm water with a mild detergent, and dry them fully. Wipe the housing with a damp cloth only &mdash; never hose the motor. Refit with the blade seated fully on the flat of the shaft and the grille screws firm, not over-tightened into plastic. Details per model on the <a href="/klt-series-panel-exhaust-fan" style="color:#C0392B;font-weight:600;">KLT series page</a>.</p></div>
    <div class="appcard"><h4>Wall shutter fan</h4><p>Clean the flap rails with a dry brush, then wipe with a cloth just damp with water. Do not lubricate the flaps with grease or oil: it holds dust and the flaps seize harder. If lubrication is needed, use a dry PTFE spray on the pins only. Check that every flap closes flat by hand and that no pin is bent &mdash; a single bent pin keeps the whole bank open and the fan then pulls air back through the gap when off. See <a href="/exhaust-fan-shutter-types" style="color:#C0392B;font-weight:600;">shutter types</a>.</p></div>
    <div class="appcard"><h4>Inline duct fan (BXF)</h4><p>Isolate, remove the access section or the fan body, and clean the impeller with a soft brush. Check the duct either side for lint and grease build-up &mdash; a clean impeller behind a blocked duct changes nothing. Replace the gasket if it is compressed or torn, and re-tape or re-clamp every joint you opened. Model data on the <a href="/product-inline-duct-fan" style="color:#C0392B;font-weight:600;">BXF duct fan page</a>.</p></div>
    <div class="appcard"><h4>Silent bathroom / cabinet fan</h4><p>These carry a filter or a narrow grille; both load up. Vacuum the grille first, then wash the removable parts. Never run the fan with the filter removed for long: the dust simply moves into the impeller and the motor runs hotter. Fan noise rising over months is usually a loaded filter, not a failing motor.</p></div>
  </div>

  <span class="section-tag">ELECTRICAL</span>
  <h2 class="sec">The Four Checks That Catch a Failure Early</h2>
  <p style="max-width:900px;">These need a multimeter and, for the insulation test, a 500 V insulation tester. If nobody on site has them, an electrician can complete all four in under half an hour on a whole bank of fans.</p>
  <ul style="max-width:900px;padding-left:20px;line-height:1.9;">
    <li><strong>Insulation resistance.</strong> Disconnect the fan, test winding to earth at 500 V DC. A healthy motor reads in the megohm range; a reading below 1 M&Omega; means moisture or a damaged winding, and the fan should not go back into service.</li>
    <li><strong>Running current.</strong> Clamp the live conductor and compare with the nameplate figure. Within about &plusmn;10% is normal; a high reading points to a dragging bearing or a blocked duct, a low reading to a failing capacitor.</li>
    <li><strong>Capacitor value.</strong> With the fan isolated and the capacitor discharged, measure capacitance. More than about 10% below the printed value explains a fan that hums, starts late, or runs slow.</li>
    <li><strong>Earth continuity.</strong> Confirm the earth path from the fan body to the supply earth. This is the check that gets skipped and the one that matters most on a metal housing.</li>
  </ul>
  <div class="verdict" style="background:#F8FAFC;border-left:4px solid #E21E26;padding:18px 22px;border-radius:6px;max-width:900px;margin:26px 0 46px;">
    <strong>Never test a fan with the blade removed or the duct open on a live motor.</strong> A fan running without its design resistance overspeeds, and a motor that overspeeds draws more current than it was built for.
  </div>

  <span class="section-tag">SPARES</span>
  <h2 class="sec">Spare Parts Worth Keeping on Site</h2>
  <p style="max-width:900px;">For a site with more than about twenty fans, holding a small spares box turns a two-week wait into a same-day repair. These are the parts we ship most often, and they are available for any model we have supplied.</p>

  <div class="twrap">
  <table class="spec-table">
  <tr><th>Part</th><th>Why keep it</th><th>How to order it correctly</th></tr>
  <tr><td>Run capacitor</td><td>First failure item, cheap, and the fan is unusable without it</td><td>Model plus the &micro;F value printed on the old capacitor (or a photo of the nameplate)</td></tr>
  <tr><td>Blade / impeller</td><td>Impact damage or a blade run out of balance after years of dust</td><td>Model, blade diameter, and a photo of the blade hub</td></tr>
  <tr><td>Motor</td><td>Lets you repair a unit where the housing and shutter are still good</td><td>Model, voltage, frequency, and the date code from the label</td></tr>
  <tr><td>Shutter flap set / spring</td><td>The most common non-electrical failure on wall fans</td><td>Model and frame size; flap sets are matched to the frame, not universal</td></tr>
  <tr><td>Gasket and fixing kit</td><td>Every duct or wall re-fit needs one; a compressed gasket leaks air and water</td><td>Model and the mounting type (wall, window, duct)</td></tr>
  </table>
  </div>
  <p class="tnote">Send the model and the date code from the fan label when ordering spares &mdash; a photo of the label is enough. Parts are matched to the production batch, and the same model can carry different motors across years.</p>

  <span class="section-tag">DECISION</span>
  <h2 class="sec">Repair or Replace</h2>
  <p style="max-width:900px;">Three rules cover almost every case:</p>
  <ol style="max-width:900px;padding-left:22px;line-height:1.9;">
    <li><strong>Capacitor, gasket, shutter flap, blade:</strong> always repair. These are consumables and the repair is a fraction of a new fan.</li>
    <li><strong>Bearing noise on a small panel fan:</strong> usually replace the unit. The motor is most of the cost, and the housing rarely survives a second service without cracking.</li>
    <li><strong>Third repair on the same unit:</strong> replace it. Repeat failures point to an installation problem &mdash; undersized duct, missing make-up air, or a fan running outside its curve &mdash; and a new fan on the same bad installation will fail the same way. Check the sizing before you re-order: the <a href="/exhaust-fan-airflow-calculation-guide" style="color:#C0392B;font-weight:600;">airflow calculation guide</a> and the <a href="/cfm-calculator" style="color:#C0392B;font-weight:600;">CFM calculator</a> both cover this.</li>
  </ol>

  <span class="section-tag">WARRANTY</span>
  <h2 class="sec">What the Warranty Covers, and What It Does Not</h2>
  <p style="max-width:900px;">Our standard warranty is 12 months on PP housing and blade models and 24 months on ABS models, against manufacturing defects from the date of shipment. Defective units are replaced or refunded after photo or video confirmation. It does not cover dust-blocked impellers, seized shutters, water ingress from hosing, or a motor destroyed by a failed capacitor that was left humming for weeks &mdash; which is exactly why the schedule above exists.</p>

  <div class="faqwrap">
    <details open>
      <summary>How often should an exhaust fan be cleaned? <span>+</span></summary>
      <div class="fa">It depends on the air. A home bathroom fan needs a clean every six months. A workshop, welding bay or woodworking shop needs it every one to three months, and every month if the fan runs 24 hours. Kitchen extraction is set by grease rather than dust: clean the impeller every one to three months and put the duct on the fire-code schedule for the building.</div>
    </details>
    <details>
      <summary>Can I wash the fan with a hose? <span>+</span></summary>
      <div class="fa">No. Wash the blade and grille off the fan, dry them, and wipe the housing with a damp cloth. Water reaching the winding is the one failure that cannot be repaired and is not covered by warranty. On duct fans, keep water out of the motor housing and out of the duct itself.</div>
    </details>
    <details>
      <summary>My fan hums but will not spin &mdash; is it finished? <span>+</span></summary>
      <div class="fa">Usually not. A hum with no rotation is the classic failed run capacitor, and it is the cheapest repair on the fan. Isolate the supply, discharge and replace the capacitor with the same microfarad value. If the fan still will not start with a good capacitor, the bearing is seized or the winding is gone and the motor should be replaced.</div>
    </details>
    <details>
      <summary>Why does the shutter stay open when the fan is off? <span>+</span></summary>
      <div class="fa">Either the flaps are dirty in the rails, a pin is bent, a spring has stretched, or someone lubricated the flaps with grease and it has collected grit. Clean the rails dry, straighten the pins, replace the flap set if the plastic is worn, and use at most a dry PTFE spray. A shutter that stays open lets air, dust and rain back in and makes the fan look like it is running when it is not.</div>
    </details>
    <details>
      <summary>Do I need to lubricate the motor? <span>+</span></summary>
      <div class="fa">No. The motors we fit use sealed bearings that cannot be re-greased. Adding oil at the shaft does nothing useful and can wash out the seal. When a sealed bearing starts to rumble, the practical fix is a new motor or a new fan.</div>
    </details>
    <details>
      <summary>Can I replace just the motor instead of the whole fan? <span>+</span></summary>
      <div class="fa">On duct fans and larger wall fans, yes, and it is usually worth it &mdash; the housing, shutter and duct connection stay in place. On small panel and bathroom fans the motor is most of the unit cost, so replacement of the whole fan is normally cheaper than the labour. Send the model and the date code from the label and we will confirm which applies.</div>
    </details>
    <details>
      <summary>How do I store fans between installation phases? <span>+</span></summary>
      <div class="fa">Keep them in the carton, dry, off a concrete floor, and out of direct sun. Do not stack more than the carton is rated for. If a fan has been installed but the building is not in use, run it for ten minutes a month: it moves moisture out of the winding and stops the bearing sitting in one position. In coastal or Gulf humidity, add a moisture absorber to the store.</div>
    </details>
    <details>
      <summary>Does a dirty fan use more electricity? <span>+</span></summary>
      <div class="fa">It uses about the same electricity to move less air. A fouled impeller and a loaded filter push the fan up its curve, so the airflow falls while the motor keeps drawing near nameplate current. The bill barely changes; the ventilation does, which is the part nobody notices until the room is hot or the extract stops clearing fumes.</div>
    </details>
    <details>
      <summary>What is the maintenance difference between a dusty workshop and a kitchen? <span>+</span></summary>
      <div class="fa">Dust is dry and blocks the blade leading edge; grease is sticky and coats the whole impeller and the duct wall behind it. Dust can be brushed off on site. Grease needs a degreaser and, in a commercial kitchen, a duct clean on the schedule the fire code sets for the building. For duct-led kitchen layouts see the <a href="/commercial-kitchen-exhaust-fans" style="color:#C0392B;font-weight:600;">kitchen exhaust page</a>; for dusty production halls see <a href="/industrial-exhaust-fans" style="color:#C0392B;font-weight:600;">industrial exhaust fans</a>.</div>
    </details>
  </div>

  <h2 class="sec">Related Guides</h2>
  <div class="appgrid">
    <div class="appcard"><h4><a href="/exhaust-fan-sizes-guide" style="color:#0F172A;">Sizes Guide</a></h4><p>What each nominal size delivers, and how to measure the opening you actually have.</p></div>
    <div class="appcard"><h4><a href="/exhaust-fan-airflow-calculation-guide" style="color:#0F172A;">Airflow Calculation</a></h4><p>Room volume, air changes per hour, static pressure and how to pick the model.</p></div>
    <div class="appcard"><h4><a href="/panel-exhaust-fan-installation-guide" style="color:#0F172A;">Installation Guide</a></h4><p>Cut-out size, mounting height, wiring and the mistakes made on site.</p></div>
    <div class="appcard"><h4><a href="/exhaust-fan-shutter-types" style="color:#0F172A;">Shutter Types</a></h4><p>Flap materials and mechanisms, and why a shutter jams when it is greased.</p></div>
  </div>

  <div class="ctabox">
    <h2>Need a Spare, or a Second Opinion on a Failing Unit?</h2>
    <p>Send the model and the date code from the fan label (a photo is enough), a short description of what it is doing, and the quantity you need. We will confirm the part, the compatibility and the lead time &mdash; usually within one working day.</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">WhatsApp: +86 136 5585 9122</a>
      <a class="btn btn-red" href="/contact/">Send Inquiry</a>
      <a class="btn btn-ghost" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
    </div>
  </div>

</div>
"""

# ---------- footer + floating, verbatim ----------
footer_i = shell.find("<footer")
ld_i = shell.find('<script type="application/ld+json">')
tail = shell[footer_i:ld_i]

LD = f"""<script type="application/ld+json">{{"@context": "https://schema.org", "@graph": [{{"@type": ["WebPage", "Article"], "@id": "{URL}", "url": "{URL}", "headline": "Exhaust Fan Maintenance: What Fails First, and What to Do Each Quarter", "description": "A 12-month maintenance schedule for wall, panel and duct exhaust fans: failure order, cleaning method by fan type, electrical checks, spare parts and repair-or-replace rules.", "isPartOf": {{"@id": "https://baer-ventilation.com/#website"}}, "inLanguage": "en", "datePublished": "2026-11-03", "dateModified": "2026-11-03", "author": {{"@id": "https://baer-ventilation.com/#organization"}}, "publisher": {{"@id": "https://baer-ventilation.com/#organization"}}, "breadcrumb": {{"@id": "{URL}#breadcrumb"}}}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": "{URL}#breadcrumb", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://baer-ventilation.com/"}}, {{"@type": "ListItem", "position": 2, "name": "Products", "item": "https://baer-ventilation.com/products/"}}, {{"@type": "ListItem", "position": 3, "name": "Exhaust Fan Maintenance", "item": "{URL}"}}]}}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "FAQPage", "@id": "{URL}#faq", "mainEntity": [{{"@type": "Question", "name": "How often should an exhaust fan be cleaned?", "acceptedAnswer": {{"@type": "Answer", "text": "It depends on the air. A home bathroom fan needs a clean every six months. A workshop, welding bay or woodworking shop needs it every one to three months, and every month if the fan runs 24 hours. Kitchen extraction is set by grease rather than dust: clean the impeller every one to three months and put the duct on the fire-code schedule for the building."}}}}, {{"@type": "Question", "name": "Can I wash the fan with a hose?", "acceptedAnswer": {{"@type": "Answer", "text": "No. Wash the blade and grille off the fan, dry them, and wipe the housing with a damp cloth. Water reaching the winding is the one failure that cannot be repaired and is not covered by warranty. On duct fans, keep water out of the motor housing and out of the duct itself."}}}}, {{"@type": "Question", "name": "My fan hums but will not spin - is it finished?", "acceptedAnswer": {{"@type": "Answer", "text": "Usually not. A hum with no rotation is the classic failed run capacitor, and it is the cheapest repair on the fan. Isolate the supply, discharge and replace the capacitor with the same microfarad value. If the fan still will not start with a good capacitor, the bearing is seized or the winding is gone and the motor should be replaced."}}}}, {{"@type": "Question", "name": "Why does the shutter stay open when the fan is off?", "acceptedAnswer": {{"@type": "Answer", "text": "Either the flaps are dirty in the rails, a pin is bent, a spring has stretched, or someone lubricated the flaps with grease and it has collected grit. Clean the rails dry, straighten the pins, replace the flap set if the plastic is worn, and use at most a dry PTFE spray. A shutter that stays open lets air, dust and rain back in and makes the fan look like it is running when it is not."}}}}, {{"@type": "Question", "name": "Do I need to lubricate the motor?", "acceptedAnswer": {{"@type": "Answer", "text": "No. The motors we fit use sealed bearings that cannot be re-greased. Adding oil at the shaft does nothing useful and can wash out the seal. When a sealed bearing starts to rumble, the practical fix is a new motor or a new fan."}}}}, {{"@type": "Question", "name": "Can I replace just the motor instead of the whole fan?", "acceptedAnswer": {{"@type": "Answer", "text": "On duct fans and larger wall fans, yes, and it is usually worth it - the housing, shutter and duct connection stay in place. On small panel and bathroom fans the motor is most of the unit cost, so replacement of the whole fan is normally cheaper than the labour. Send the model and the date code from the label and we will confirm which applies."}}}}, {{"@type": "Question", "name": "How do I store fans between installation phases?", "acceptedAnswer": {{"@type": "Answer", "text": "Keep them in the carton, dry, off a concrete floor, and out of direct sun. Do not stack more than the carton is rated for. If a fan has been installed but the building is not in use, run it for ten minutes a month: it moves moisture out of the winding and stops the bearing sitting in one position. In coastal or Gulf humidity, add a moisture absorber to the store."}}}}, {{"@type": "Question", "name": "Does a dirty fan use more electricity?", "acceptedAnswer": {{"@type": "Answer", "text": "It uses about the same electricity to move less air. A fouled impeller and a loaded filter push the fan up its curve, so the airflow falls while the motor keeps drawing near nameplate current. The bill barely changes; the ventilation does, which is the part nobody notices until the room is hot or the extract stops clearing fumes."}}}}, {{"@type": "Question", "name": "What is the maintenance difference between a dusty workshop and a kitchen?", "acceptedAnswer": {{"@type": "Answer", "text": "Dust is dry and blocks the blade leading edge; grease is sticky and coats the whole impeller and the duct wall behind it. Dust can be brushed off on site. Grease needs a degreaser and, in a commercial kitchen, a duct clean on the schedule the fire code sets for the building."}}}}]}}</script>
</body>
</html>
"""

# table CSS for this page (house style, matching country pages)
TBL_CSS = """/* spec tables */
.twrap{overflow-x:auto;margin:0 0 6px;}
.spec-table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;}
.spec-table th{background:var(--dark);color:#fff;padding:11px 14px;text-align:left;font-weight:700;font-size:13px;}
.spec-table td{padding:11px 14px;border-bottom:1px solid var(--line);color:var(--text);vertical-align:top;}
.spec-table tr:nth-child(even) td{background:var(--light);}
.spec-table a{color:#C0392B;font-weight:700;}
.tnote{font-size:12.5px;color:var(--muted);margin:8px 0 46px;line-height:1.7;}
@media(max-width:768px){.spec-table{font-size:12.5px;}.spec-table th,.spec-table td{padding:9px 10px;}}
"""

# inject the table CSS just before the second </style> (the topbar block ends the head)
head = head.replace("</style>", TBL_CSS + "</style>", 1)

out = head + "</head>" + prefix + HERO + CRUMB + '<div class="container">\n' + BODY + tail + LD
out = out.replace("\r\n", "\n").replace("\n", "\r\n")

open(SITE + SLUG + ".html", "wb").write(out.encode("utf-8"))
print("written", len(out), "chars")

# ---- self checks ----
for bad in ["sizes-guide", "exhaust-fan-sizes", "4, 6, 8, 10, 12", "H42e66"]:
    pass
print("leftover sizes-guide mentions:", out.count("sizes-guide"))
print("leftover product-page slugs:", sum(out.count(s) for s in ["product-klt-10b", "product-window-fan", "6inch"]))
print("h1 count:", out.count("<h1"))
print("jsonld blocks:", out.count('type="application/ld+json"'))
print("tables:", out.count('class="spec-table"'))
