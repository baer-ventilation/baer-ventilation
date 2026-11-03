# -*- coding: utf-8 -*-
"""1) shutter-types: commercial submittal section  2) factory-walkthrough inbound links  3) trim 4 long descriptions"""
import re

SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"

def load(fn): return open(SITE + fn, "rb").read().decode("utf-8")
def save(fn, s): open(SITE + fn, "wb").write(s.encode("utf-8"))

def rep(fn, old, new, label):
    s = load(fn)
    c = s.count(old)
    if c != 1:
        print(f"  !! {fn} [{label}] matches={c} -- SKIP")
        return
    save(fn, s.replace(old, new))
    print(f"  ok {fn} [{label}]")

# ---------------- 1. shutter submittal section ----------------
SECTION = """<h2>Writing a Shutter Into a Commercial Submittal</h2>
  <p>On a commercial job the shutter is usually one line on the ventilation schedule, and a reviewer looks at it the way they look at any louvre: free area, pressure drop, material, control and corrosion class. Getting those five fields right at submittal stage prevents the expensive version of this problem &mdash; a fan sized for a free opening, with a shutter taking 40 Pa out of a system that had no headroom to lose.</p>
  <div class="table-scroll">
  <table class="compare-table">
    <thead><tr><th>Field</th><th>What to state</th><th>Why the reviewer asks</th></tr></thead>
    <tbody>
      <tr><td>Free area</td><td>Open area at full open, in m&sup2; or as a percentage of the frame</td><td>A single-bank gravity shutter typically gives 45&ndash;60% of its frame area. A &ldquo;500 &times; 500 shutter&rdquo; is often nearer 0.13 m&sup2; open than 0.25 m&sup2; &mdash; while the duct calculation used the larger figure.</td></tr>
      <tr><td>Pressure drop at design flow</td><td>Pa at the design face velocity, taken from the model data</td><td>Typically 20&ndash;40 Pa at 8&ndash;10 m/s. If it is not on the schedule, nobody adds it to the fan duty.</td></tr>
      <tr><td>Face velocity</td><td>Design velocity in m/s at the shutter</td><td>Above about 12 m/s the flaps lift and rattle in wind and rain carries past the blades. External walls are normally held at 8&ndash;10 m/s.</td></tr>
      <tr><td>Materials and finish</td><td>Frame material, flap material, coating</td><td>Galvanised frame with aluminium flaps is the norm for coastal and industrial sites; ABS suits light commercial and residential. Naming the environment is what allows the finish to be matched.</td></tr>
      <tr><td>Actuator and fail position</td><td>230 V on/off or 24 V with spring return, and what happens on power failure</td><td>Spring return closes the shutter when the fan stops. A plain on/off actuator leaves a hole in the wall after a trip or a fire-alarm test.</td></tr>
      <tr><td>Mounting position</td><td>Inside the wall, or on the external face</td><td>It sets the frame depth and the fixing method, and decides whether an insect screen or weather hood is needed in front of the flaps.</td></tr>
      <tr><td>Fire compartment</td><td>Whether the wall is fire-rated</td><td>A shutter is not a fire damper and must never be submitted as one. On a compartment wall the damper is a separate, certified item.</td></tr>
    </tbody>
  </table>
  </div>
  <p><strong>The one number worth re-checking.</strong> When a schedule says &ldquo;louvre 500 &times; 500&rdquo;, confirm whether that is the frame or the free area. At the same airflow, the difference between a 0.25 m&sup2; frame and 0.13 m&sup2; free area is a 45% jump in face velocity &mdash; which is the difference between a shutter that sits flat and one that rattles all night and lets rain in.</p>
  <p><strong>What to attach.</strong> Four documents settle most submittal comments: a dimensioned drawing with the frame and free area marked, the pressure-drop figure at design flow, the actuator wiring diagram with the fail position stated, and the material or coating statement. All four are issued with our project quotations &mdash; ask at RFQ stage rather than after the order, because the free area figure sometimes changes the fan selection.</p>
  <p><strong>Who supplies what.</strong> We supply the fan and its matched shutter as one item &mdash; factory-fitted, or as a separate frame for site assembly where the wall is built first. Insect screens, weather hoods, fire dampers and BMS controls are normally specified and supplied by the MEP contractor. Tell us what is going around our unit and we will confirm the clearances, the duct connection and the wiring interface. For large banks on an industrial wall, the air-change table in the <a href="/industrial-exhaust-fans">industrial exhaust fan guide</a> is the starting point; for how often the pins behind a shutter need cleaning in a dusty or coastal plant, see the <a href="/exhaust-fan-maintenance-guide">maintenance schedule</a>.</p>
  """

rep("exhaust-fan-shutter-types.html",
    "<h2>Which to Specify by Climate and Application</h2>",
    SECTION + "<h2>Which to Specify by Climate and Application</h2>",
    "submittal-section")

# ---------------- 2. factory-walkthrough inbound links ----------------
rep("baer-production-capacity.html",
    "<strong>Live video tours:</strong> a walking walkthrough of the lines you care about",
    '<strong>Live video tours:</strong> a <a href="/baer-factory-walkthrough" style="color:#C0392B;font-weight:700;">walking walkthrough</a> of the lines you care about',
    "walkthrough-link")

rep("how-to-verify-china-exhaust-fan-manufacturer.html",
    "A recorded tour can be years old; a live call cannot be faked easily.",
    'A recorded tour can be years old; a live call cannot be faked easily. Our own <a href="/baer-factory-walkthrough" style="color:#C0392B;font-weight:700;">factory walkthrough</a> shows what the inside of an injection-moulding, winding and assembly plant looks like, so you know what to look for on the call.',
    "walkthrough-link")

# ---------------- 3. trim the four over-long descriptions ----------------
DESC = {
 "exhaust-fan-sizes-guide.html": (
   "What 4, 6, 8, 10, 12 and 18 inch exhaust fans actually deliver: airflow per size, room coverage, wall cut-out dimensions and why the same nominal size ranges from 150 to 1,670 m3/h.",
   "What 4, 6, 8, 10, 12 and 18 inch exhaust fans actually deliver: airflow per size, room coverage, wall cut-out, and why one size spans 150 to 1,670 m3/h."),

 "commercial-kitchen-exhaust-fans.html": (
   "Ducted BXF mixed-flow exhaust fans for cafe, restaurant, canteen and dishwash extract: hood length sizing, duct velocity band and pressure budget for real installs.",
   "Ducted BXF mixed-flow fans for cafe, restaurant, canteen and dishwash extract: hood sizing, duct velocity, pressure budget and make-up air."),

 "industrial-exhaust-fans.html": (
   "Industrial exhaust fans for warehouses, workshops and factories: 984 to 4,500 CFM wall shutter, axial and ducted fans, with an air-change sizing table by space type.",
   "Industrial exhaust fans for warehouses, workshops and loading areas: 984-4,500 CFM shutter and ducted fans, plus an air-change sizing table."),

 "baer-production-capacity.html": (
   "Inside the BAER factory in Shengzhou, Zhejiang: 4 workshops, 50,000 m2 of production buildings, 12 injection moulding machines, in-house motor winding, 8 assembly lines and 1,000,000 fans a year.",
   "Inside the BAER factory in Shengzhou: 4 workshops, 50,000 m2 of production buildings, 12 injection moulders, in-house winding, 1,000,000 fans a year."),
}
for fn, (old, new) in DESC.items():
    if len(old) == 0:
        continue
    rep(fn, f'<meta name="description" content="{old}">',
        f'<meta name="description" content="{new}">', "desc-trim")
print("done")
