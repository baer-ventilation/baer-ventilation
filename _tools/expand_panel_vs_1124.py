# -*- coding: utf-8 -*-
"""Insert-only expansion of panel-fan-vs-axial-fan-vs-inline-fan.html.
Keeps all existing structure (VideoObject, styles, video iframe). Adds sections,
4 tables, 11 photos (12 total), 3 schematics, 2 FAQs. CRLF preserved byte-wise.
Idempotent: each insertion guarded by a unique marker already in the file.
"""
import sys, re, json

PATH = 'panel-fan-vs-axial-fan-vs-inline-fan.html'
APPLY = '--apply' in sys.argv
raw = open(PATH, 'rb').read()
assert raw.count(b'\n') == raw.count(b'\r\n'), 'not pure CRLF - abort'
s = raw.decode('utf-8')

def crlf(t):
    return t.replace('\n', '\r\n')

ops = []  # (marker, old, new, label)

# ---------- 1. How the three families actually work (before "Why Pressure") ----------
marker1 = 'id="how-they-work"'
new1 = crlf('''  <h2 id="how-they-work">How the Three Families Actually Move Air</h2>
  <p>The labels describe how the impeller and housing are built, not three unrelated machines. Understanding the mechanism makes the pressure and noise differences predictable, instead of a list of numbers to memorise.</p>
  <h3>Panel fan — a propeller in a wall plate</h3>
  <p>A panel (wall or window) fan is an axial propeller mounted in a square flange that sits flush with a wall. Air approaches along the shaft, passes the blades and leaves on the same axis. It is built for volume at almost zero resistance: one 12-inch KLT-20B moves 792 m&sup3;/h in free air. The square plate, shutters and simple two-pole motor keep it the cheapest option per cubic metre delivered. Its weakness is pressure — add duct and the free-air number collapses.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/baer-panel-fan-klt-front.webp" alt="BAER KLT series panel exhaust fan front view" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">KLT panel fan: axial propeller in a wall plate, the lowest-cost option for a direct wall opening.</figcaption>
  </figure>
  <h3>Cased axial fan — the propeller in a tube</h3>
  <p>Put the same axial propeller inside a cylindrical case and it can be fitted into a short duct or wall sleeve. The case directs the flow and gives a little more pressure capability, but the physics is unchanged: high flow, low pressure, and a steep fall-off once system resistance climbs. It occupies the narrow middle ground between a bare wall fan and a true duct fan.</p>
  <h3>Inline mixed-flow fan — axial in, swirled out</h3>
  <p>An inline mixed-flow impeller adds a radial component to the axial flow. Air enters along the shaft but leaves at an angle, so the fan develops real static pressure while keeping a compact cylindrical housing. That pressure is what makes a 10-metre duct run work. It costs more because the impeller, casing and motor bearings are all specified for a harder duty.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/baer-inline-duct-fan-shelf.webp" alt="BAER inline duct fans on the sample room shelf" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Inline mixed-flow models: a slimmer free-air rating, but the pressure to push air through real ductwork.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <svg viewBox="0 0 720 230" width="100%" role="img" aria-label="Schematic of airflow paths for panel, cased axial and inline mixed-flow fans" style="max-width:720px;height:auto;background:#F8FAFC;border-radius:8px;">
      <text x="360" y="22" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#1E293B">Air path by fan family</text>
      <text x="360" y="215" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#94A3B8">Schematic only — airflow direction illustration, not measured BAER data</text>
      <g font-family="Arial,sans-serif" font-size="12" fill="#475569">
        <text x="20" y="62" font-weight="700" fill="#1E293B">Panel / wall</text>
        <rect x="120" y="46" width="90" height="34" fill="#FEE2E2" stroke="#C0392B" stroke-width="2" rx="4"/>
        <path d="M125 63 L205 63" stroke="#C0392B" stroke-width="2.5" marker-end="url(#ar)"/>
        <text x="225" y="67">straight through, no duct</text>

        <text x="20" y="122" font-weight="700" fill="#1E293B">Cased axial</text>
        <rect x="120" y="106" width="90" height="34" fill="#FEF3C7" stroke="#D97706" stroke-width="2" rx="4"/>
        <path d="M125 123 L205 123" stroke="#D97706" stroke-width="2.5" marker-end="url(#ar)"/>
        <text x="225" y="127">straight, short duct only</text>

        <text x="20" y="182" font-weight="700" fill="#1E293B">Inline mixed-flow</text>
        <rect x="120" y="166" width="90" height="34" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="2" rx="4"/>
        <path d="M125 183 L195 183" stroke="#1D4ED8" stroke-width="2.5"/>
        <path d="M195 183 L225 172 M195 183 L225 194" stroke="#1D4ED8" stroke-width="2.5" marker-end="url(#ar)"/>
        <text x="235" y="187">axial in, angled out → pressure</text>
      </g>
      <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6" fill="#475569"/></marker></defs>
    </svg>
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">The housing and impeller decide pressure capability — the single most important selection input.</figcaption>
  </figure>

''')
ops.append((marker1, '  <h2>Why Pressure Is the Deciding Factor</h2>', new1 + '  <h2>Why Pressure Is the Deciding Factor</h2>', 'how-they-work section'))

# ---------- 2. Static pressure numbers + 10m trap (after physics paragraph) ----------
anchor2 = '  <p>For the physics in more detail, and a two-way comparison of the ducted options, see <a href="/inline-duct-fan-vs-axial-fan">Inline Duct Fan vs Axial Fan</a>.</p>'
marker2 = 'id="static-pressure-numbers"'
new2 = crlf('''  <h2 id="static-pressure-numbers">Static Pressure by Family: Typical Industry Ranges</h2>
  <p>These are published industry ranges for each family, not BAER test certificates — use them to shortlist a type, then request the performance curve for the exact model. The practical message is the spread: an inline mixed-flow fan develops several times the pressure of a wall fan, which is why it is the default wherever duct length is real.</p>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th>Family</th><th>Typical static pressure</th><th>Peak efficiency</th><th>Behaviour as resistance rises</th></tr></thead>
    <tbody>
      <tr><td>Panel / wall axial</td><td>~50–150 Pa</td><td>~40–60%</td><td>Airflow drops sharply; can stall behind duct</td></tr>
      <tr><td>Cased axial</td><td>~50–300 Pa</td><td>~50–70%</td><td>Moderate drop; short runs only</td></tr>
      <tr><td>Inline mixed-flow</td><td>~200–1,000 Pa</td><td>~65–80%</td><td>Holds airflow across a wider pressure band</td></tr>
      <tr><td>Centrifugal (for reference)</td><td>~500–3,000+ Pa</td><td>~70–90%</td><td>Best for very high resistance, larger and costlier</td></tr>
    </tbody>
  </table>
  </div>
  <p class="note" style="background:#FFFBEB;border-left:4px solid #F59E0B;padding:16px 20px;border-radius:6px;margin:24px 0;font-size:14.5px;color:#475569;">Ranges are indicative industry figures compiled from public manufacturer and engineering references. Always specify against a model's tested pressure–flow curve; never size from free-air m&sup3;/h alone.</p>

  <h2 id="duct-run-trap">The 10-Metre Duct-Run Trap</h2>
  <p>The most common selection failure is choosing on free-air airflow and ignoring the duct. A wall fan rated 792 m&sup3;/h with nothing attached may deliver less than half that behind 10 metres of duct and two bends, because every metre of straight duct and every elbow adds resistance. The fan has to generate enough pressure to overcome it — and a panel fan simply cannot.</p>
  <figure style="margin:26px 0;text-align:center;">
    <svg viewBox="0 0 720 260" width="100%" role="img" aria-label="Schematic showing airflow falling as duct length increases for panel versus inline fans" style="max-width:720px;height:auto;background:#F8FAFC;border-radius:8px;">
      <text x="360" y="22" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#1E293B">Delivered airflow vs duct length</text>
      <line x1="90" y1="210" x2="680" y2="210" stroke="#94A3B8" stroke-width="1.5"/>
      <line x1="90" y1="210" x2="90" y2="45" stroke="#94A3B8" stroke-width="1.5"/>
      <text x="80" y="50" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#64748b">high</text>
      <text x="80" y="214" text-anchor="end" font-family="Arial,sans-serif" font-size="11" fill="#64748b">low</text>
      <text x="385" y="240" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" fill="#475569">Duct length / resistance →</text>
      <path d="M95 60 Q 300 120 430 195" fill="none" stroke="#C0392B" stroke-width="3"/>
      <path d="M95 70 Q 350 90 660 120" fill="none" stroke="#1D4ED8" stroke-width="3"/>
      <text x="200" y="95" font-family="Arial,sans-serif" font-size="12" font-weight="700" fill="#C0392B">Panel / axial</text>
      <text x="470" y="103" font-family="Arial,sans-serif" font-size="12" font-weight="700" fill="#1D4ED8">Inline mixed-flow</text>
      <text x="360" y="255" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#94A3B8">Schematic only — illustrative trend, not measured BAER test data</text>
    </svg>
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">The axial curve falls away with resistance; the mixed-flow curve holds. Exact figures come from the model's test report.</figcaption>
  </figure>
  <p>Rule of thumb from installers: a panel fan is acceptable direct-through-wall or up to about 3 metres of straight rigid duct, with 15–30% allowed off the free-air rating. Beyond roughly 5 metres, or with two or more bends, move to an inline fan. If the run has filters, a hood or a long vertical rise, the resistance climbs again — size from the curve, not the catalogue headline.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/baer-inline-fan-cutaway.webp" alt="Cutaway of a BAER inline duct fan showing impeller and casing" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">The mixed-flow impeller and close-fitting casing are what generate pressure in a long duct run.</figcaption>
  </figure>

''')
ops.append((marker2, anchor2, anchor2 + crlf('\n') + new2, 'static-pressure + duct-trap sections'))

# ---------- 3. Noise section (before "When to Use Both") ----------
marker3 = 'id="noise-location"'
new3 = crlf('''  <h2 id="noise-location">Noise: Where the Fan Sits Matters More Than the dB Number</h2>
  <p>A dB figure in a catalogue is usually measured at the fan inlet in a laboratory. What a room occupant hears depends mainly on distance and barriers. Moving the fan out of the occupied space is the single most effective acoustic measure — more effective than shaving a few decibels off the motor.</p>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th>Installation</th><th>Where the noise goes</th><th>Typical result in the room</th><th>Notes</th></tr></thead>
    <tbody>
      <tr><td>Panel fan in the wall</td><td>Directly into the room</td><td>Most noticeable</td><td>Add a shutter; keep blades clean and bearings sound</td></tr>
      <tr><td>Cased axial in a short sleeve</td><td>Partly into the room, partly outside</td><td>Moderate</td><td>Short runs only; case helps direct the flow</td></tr>
      <tr><td>Inline fan in a ceiling void</td><td>Into the void, away from occupants</td><td>Quietest</td><td>Use a short flexible drop to the grille; isolate vibration</td></tr>
    </tbody>
  </table>
  </div>
  <p>For a hotel bathroom or a bedroom, the quiet specification is an inline mixed-flow fan above the ceiling with a short flexible connector. A panel fan in the wall always radiates into the room, no matter how low its stated dB. Flexible mounts and a correctly sized grille keep the duct from transmitting structure-borne noise.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/inline-impellers.webp" alt="Inline fan impellers of various diameters" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">A larger, slower impeller moves the same air with less blade noise — one reason to avoid undersizing.</figcaption>
  </figure>

''')
ops.append((marker3, '  <h2>When to Use Both</h2>', new3 + '  <h2>When to Use Both</h2>', 'noise-location section'))

# ---------- 4. Installation & maintenance trade-offs (before "Common Mistakes") ----------
marker4 = 'id="install-maintenance"'
new4 = crlf('''  <h2 id="install-maintenance">Installation and Maintenance Trade-offs</h2>
  <p>Selection is not only about performance on day one. The three families differ in how they are installed, how easily they are cleaned, and how long they stay quiet — all of which affect lifetime cost more than the purchase price.</p>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th>Factor</th><th>Panel fan</th><th>Cased axial</th><th>Inline mixed-flow</th></tr></thead>
    <tbody>
      <tr><td>Install effort</td><td>Cut one wall opening, fix four screws</td><td>Fit into sleeve or short duct</td><td>Mount in duct/void, wire to remote switch</td></tr>
      <tr><td>Access for cleaning</td><td>Front shutters lift off</td><td>Remove the case section</td><td>Access panel in duct required</td></tr>
      <tr><td>Dust / grease tolerance</td><td>Low — keep blades clean</td><td>Low to moderate</td><td>Moderate — add filters upstream</td></tr>
      <tr><td>Bearing / motor duty</td><td>Light</td><td>Light to moderate</td><td>Higher pressure, better bearings specified</td></tr>
      <tr><td>Typical service life factor</td><td>Shortest in dirty, hot sites</td><td>Middle</td><td>Longest when correctly sized</td></tr>
    </tbody>
  </table>
  </div>
  <p>A panel fan in a dusty workshop will accumulate blade dust, lose airflow and grow noisy unless it is cleaned. An inline fan hidden in a ceiling void is quieter but must be accessible for service — specify an access panel at order stage. Whatever the family, an undersized fan running at the wrong point on its curve is the fastest route to noise and premature bearing failure.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/panel-fan-assembly-line.webp" alt="BAER panel fan assembly line" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Panel fans on the assembly line: simple construction keeps unit cost low, but installation quality still decides performance.</figcaption>
  </figure>

''')
ops.append((marker4, '  <h2>Common Mistakes</h2>', new4 + '  <h2>Common Mistakes</h2>', 'install-maintenance section'))

# ---------- 5. Worked example + what to tell supplier (before FAQ) ----------
marker5 = 'id="worked-example"'
new5 = crlf('''  <h2 id="worked-example">A Worked Selection Example</h2>
  <p>Two buyers both need 500 m&sup3;/h. Buyer A extracts directly through an external kitchen wall — no duct. A KLT panel fan is the correct call: lowest cost, easiest install, and the free-air rating is nearly the delivered airflow. Buyer B needs the same 500 m&sup3;/h in an internal bathroom with an 8-metre duct and two bends to the facade. The panel fan would stall; size an inline mixed-flow fan from its curve at the estimated system pressure, allow for the bends, and mount it in the ceiling void for quiet operation. Same airflow target, different family — that is the whole decision in one example.</p>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th>Question to answer first</th><th>If yes →</th><th>If no →</th></tr></thead>
    <tbody>
      <tr><td>Is the wall external and the run under ~3 m?</td><td>Panel fan</td><td>Keep going</td></tr>
      <tr><td>Is the run over ~5 m, or are there 2+ bends?</td><td>Inline mixed-flow</td><td>Cased axial may be enough</td></tr>
      <tr><td>Is noise in the room critical (hotel, bedroom)?</td><td>Inline in the void</td><td>Panel acceptable</td></tr>
      <tr><td>Is resistance high (filters, hood, long rise)?</td><td>Inline; check the curve</td><td>Axial short run</td></tr>
      <tr><td>Is lowest unit cost the priority?</td><td>Panel fan</td><td>Size for the duty</td></tr>
    </tbody>
  </table>
  </div>
  <figure style="margin:26px 0;text-align:center;">
    <svg viewBox="0 0 720 300" width="100%" role="img" aria-label="Schematic decision tree for choosing a panel, cased axial or inline fan" style="max-width:720px;height:auto;background:#F8FAFC;border-radius:8px;">
      <text x="360" y="22" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#1E293B">Selection decision tree</text>
      <g font-family="Arial,sans-serif" font-size="11.5" fill="#475569" text-anchor="middle">
        <rect x="260" y="40" width="200" height="34" fill="#0f1f3d" rx="6"/><text x="360" y="62" fill="#fff" font-weight="700">Duct run &amp; resistance?</text>
        <rect x="40" y="110" width="190" height="46" fill="#FEE2E2" stroke="#C0392B" stroke-width="1.5" rx="6"/><text x="135" y="129" font-weight="700" fill="#1E293B">Direct / &lt;3 m</text><text x="135" y="146" fill="#C0392B">→ Panel fan</text>
        <rect x="265" y="110" width="190" height="46" fill="#FEF3C7" stroke="#D97706" stroke-width="1.5" rx="6"/><text x="360" y="129" font-weight="700" fill="#1E293B">Short sleeve / ~5 m</text><text x="360" y="146" fill="#D97706">→ Cased axial</text>
        <rect x="490" y="110" width="190" height="46" fill="#DBEAFE" stroke="#1D4ED8" stroke-width="1.5" rx="6"/><text x="585" y="129" font-weight="700" fill="#1E293B">&gt;5 m / 2+ bends</text><text x="585" y="146" fill="#1D4ED8">→ Inline mixed-flow</text>
        <path d="M300 74 L135 108 M360 74 L360 108 M420 74 L585 108" fill="none" stroke="#94A3B8" stroke-width="1.5"/>
        <rect x="220" y="195" width="280" height="46" fill="#F1F5F9" stroke="#64748B" stroke-width="1.5" rx="6"/><text x="360" y="214" font-weight="700" fill="#1E293B">Noise critical in the room?</text><text x="360" y="231" fill="#1D4ED8">Mount inline fan in ceiling void</text>
        <text x="360" y="278" fill="#94A3B8">Schematic only — selection heuristic; confirm with the model's test curve</text>
      </g>
    </svg>
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Start with duct length and resistance, then noise — not with the catalogue airflow number.</figcaption>
  </figure>

  <h2 id="what-to-tell-supplier">What to Tell Your Supplier for an Accurate Quote</h2>
  <p>Specify the duty, not just a model name, and a manufacturer can match the family to the job. Give: required airflow (m&sup3;/h), total duct length and number of bends, mounting position (wall, window, duct or ceiling void), supply voltage and frequency, acceptable noise level, and destination for certification requirements. With those inputs a supplier can recommend a panel, cased axial or inline model and send the matching performance curve.</p>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/baer-sample-room.webp" alt="BAER sample room showing exhaust fan models" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Samples of all three families are kept for review — ask to see the exact model, not a generic photo.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/motor-test-bench.webp" alt="BAER motor test bench" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Requests for a tested pressure–flow curve should be answered with bench data for the exact model.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/winding-station.webp" alt="BAER motor winding station" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Motor construction determines efficiency and duty life — a relevant question for 24/7 operation.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/assembly-bench-worker.webp" alt="BAER worker assembling a fan at the bench" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Assembly quality — blade balance and bearing alignment — decides how quiet a fan stays in service.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/fan-size-lineup.webp" alt="BAER exhaust fans of different diameters lined up" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Same family, different diameters — a larger, slower fan is usually quieter for the same airflow.</figcaption>
  </figure>
  <figure style="margin:26px 0;text-align:center;">
    <img src="/images/showroom-wall.webp" alt="BAER showroom wall with fan range" width="960" height="720" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">
    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Review the full range side by side before fixing a specification.</figcaption>
  </figure>

''')
ops.append((marker5, '  <h2>Frequently Asked Questions</h2>', new5 + '  <h2>Frequently Asked Questions</h2>', 'worked-example + supplier sections'))

# ---------- 6. Two more visible FAQs ----------
anchor6 = '  <p>An inline mixed-flow duct fan mounted in the ceiling void, with a short flexible drop to the ceiling grille. Moving the fan out of the room is the single most effective noise measure; a panel fan in the wall always radiates its noise into the bathroom.</p>'
marker6 = 'id="faq-duct-loss"'
new6 = crlf('''  <h3 id="faq-duct-loss">How much airflow do I lose in a long duct?</h3>
  <p>It depends on the fan's pressure capability and the duct layout, not a fixed percentage. As a planning allowance, a wall panel fan behind up to three metres of straight rigid duct may lose roughly 15–30% of its free-air rating; at ten metres with bends the loss can be far larger. An inline mixed-flow fan holds its airflow much better. Always confirm against the model's pressure–flow curve.</p>
  <h3 id="faq-centrifugal">When should I choose a centrifugal fan instead?</h3>
  <p>If system resistance is very high — long industrial duct networks, filters, dust collection or tall vertical risers — a centrifugal fan develops the pressure that even an inline mixed-flow fan cannot. It is larger and costlier, so for typical bathroom, kitchen, workshop and ceiling-void extraction an inline mixed-flow fan is the usual answer. Send your duct layout to the supplier and let them size it.</p>
''')
ops.append((marker6, anchor6, anchor6 + crlf('\n') + new6, '2 visible FAQs'))

# ---------- 7. Update visible date ----------
ops.append(('Last updated: November 24, 2026', 'Last updated: September 10, 2026', 'Last updated: November 24, 2026', 'visible date'))

# ---------- 8. JSON-LD updates: FAQPage + WebPage dateModified ----------
def update_jsonld(s):
    out = s
    # WebPage dateModified
    out = out.replace('"dateModified": "2026-09-10"', '"dateModified": "2026-11-24"', 1)
    # FAQPage: find the full <script>...</script> block whose JSON is FAQPage
    blocks = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', out, re.S))
    fb = None
    for blk in blocks:
        try:
            d = json.loads(blk.group(1))
        except Exception:
            continue
        if isinstance(d, dict) and d.get('@type') == 'FAQPage':
            fb = (blk, d)
            break
    assert fb, 'FAQPage JSON-LD not found'
    blk, d = fb
    if len(d['mainEntity']) == 5:
        d['mainEntity'].append({"@type": "Question", "name": "How much airflow do I lose in a long duct?",
            "acceptedAnswer": {"@type": "Answer", "text": "It depends on the fan's pressure capability and the duct layout, not a fixed percentage. As a planning allowance, a wall panel fan behind up to three metres of straight rigid duct may lose roughly 15-30% of its free-air rating; at ten metres with bends the loss can be far larger. An inline mixed-flow fan holds its airflow much better. Always confirm against the model's pressure-flow curve."}})
        d['mainEntity'].append({"@type": "Question", "name": "When should I choose a centrifugal fan instead?",
            "acceptedAnswer": {"@type": "Answer", "text": "If system resistance is very high - long industrial duct networks, filters, dust collection or tall vertical risers - a centrifugal fan develops the pressure that even an inline mixed-flow fan cannot. It is larger and costlier, so for typical bathroom, kitchen, workshop and ceiling-void extraction an inline mixed-flow fan is the usual answer. Send your duct layout to the supplier and let them size it."}})
        new_json = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
        out = out[:blk.start(1)] + new_json + out[blk.end(1):]
        return out, 'FAQ JSON-LD 5->7'
    return out, 'FAQ JSON-LD already updated'

# ---------- dry run / apply ----------
log = []
pending = s
for marker, old, new, label in ops:
    if marker in pending:
        log.append(('SKIP', label))
        continue
    cnt = pending.count(old)
    assert cnt == 1, '%s: anchor count %d (expected 1)' % (label, cnt)
    pending = pending.replace(old, new, 1)
    log.append(('NEW', label))

pending, jl = update_jsonld(pending)
log.append(('JSONLD', jl))

print('=== DRY RUN ===')
for st, label in log:
    print(st, label)
b = pending.encode('utf-8')
print('CRLF preserved:', b.count(b'\n') == b.count(b'\r\n'))
print('Size:', len(raw), '->', len(b))

# structural preview
t = pending
body = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
body = re.sub(r'<[^>]+>', ' ', body)
words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'&-]*", body)
print('Visible words:', len(words), '| tables:', t.count('<table'), '| imgs:', len(re.findall(r'<img', t)), '| schematics:', t.count('Schematic only'))
print('FAQ visible:', len(re.findall(r'<h3 id="faq-|Is a panel the same|Which is better|Can I use a panel|Why is an inline|What is the quietest', t)))
print('imgs without .webp:', [x for x in re.findall(r'src="(/images/[^"]+)"', t) if not x.endswith('.webp')])

if not APPLY:
    print('DRY RUN only. Pass --apply to write.')
    sys.exit(0)

open(PATH, 'wb').write(b)
print('WRITTEN')
