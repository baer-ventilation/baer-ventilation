# -*- coding: utf-8 -*-
"""Add a fan-curve section (with inline SVG chart) to the airflow calculation guide."""
import re

SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"
FN = "exhaust-fan-airflow-calculation-guide.html"

# ---------- chart geometry ----------
X0, X1, Y0, Y1 = 78, 672, 40, 344
QMAX, PMAX = 1300, 220

def sx(q): return round(X0 + q * (X1 - X0) / QMAX, 1)
def sy(p): return round(Y1 - p * (Y1 - Y0) / PMAX, 1)

fan = [(q, 190 * (1 - (q / 1250) ** 2)) for q in range(0, 1251, 125)]
sys_ = [(q, 6.8e-5 * q * q) for q in range(0, 1251, 125)]
fan_pts = " ".join(f"{sx(q)},{sy(p)}" for q, p in fan)
sys_pts = " ".join(f"{sx(q)},{sy(p)}" for q, p in sys_)

op_x, op_y = sx(1001), sy(68.1)

xticks = [0, 250, 500, 750, 1000, 1250]
yticks = [0, 50, 100, 150, 200]

xt = "\n".join(
    f'  <line x1="{sx(v)}" y1="{Y1}" x2="{sx(v)}" y2="{Y1+6}" stroke="#94A3B8" stroke-width="1"/>\n'
    f'  <text x="{sx(v)}" y="{Y1+22}" font-size="11.5" fill="#64748B" text-anchor="middle">{v:,}</text>'
    for v in xticks)
yt = "\n".join(
    f'  <line x1="{X0-6}" y1="{sy(v)}" x2="{X0}" y2="{sy(v)}" stroke="#94A3B8" stroke-width="1"/>\n'
    f'  <text x="{X0-12}" y="{sy(v)+4}" font-size="11.5" fill="#64748B" text-anchor="end">{v}</text>'
    for v in yticks)

SVG = f"""<div class="twrap" style="margin:8px 0 4px;">
<svg viewBox="0 0 720 420" width="100%" role="img" aria-label="Schematic fan curve and system resistance curve crossing at an operating point of about 1000 cubic metres per hour at 68 pascals, against a free-air rating of 1250 cubic metres per hour." style="max-width:720px;display:block;margin:0 auto;">
  <rect x="0" y="0" width="720" height="420" fill="#fff"/>
  <line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="#334155" stroke-width="1.5"/>
  <line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="#334155" stroke-width="1.5"/>
{xt}
{yt}
  <text x="{(X0+X1)//2}" y="400" font-size="12.5" fill="#0F172A" text-anchor="middle" font-weight="700">Airflow (m&#179;/h)</text>
  <text x="24" y="{(Y0+Y1)//2}" font-size="12.5" fill="#0F172A" text-anchor="middle" font-weight="700" transform="rotate(-90 24 {(Y0+Y1)//2})">Static pressure (Pa)</text>

  <polyline points="{fan_pts}" fill="none" stroke="#E21E26" stroke-width="3" stroke-linejoin="round"/>
  <polyline points="{sys_pts}" fill="none" stroke="#334155" stroke-width="2.5" stroke-dasharray="7 5"/>

  <line x1="{op_x}" y1="{op_y}" x2="{op_x}" y2="{Y1}" stroke="#E21E26" stroke-width="1" stroke-dasharray="4 4"/>
  <line x1="{X0}" y1="{op_y}" x2="{op_x}" y2="{op_y}" stroke="#E21E26" stroke-width="1" stroke-dasharray="4 4"/>
  <circle cx="{op_x}" cy="{op_y}" r="6.5" fill="#E21E26" stroke="#fff" stroke-width="2"/>

  <line x1="470" y1="60" x2="502" y2="60" stroke="#E21E26" stroke-width="3"/>
  <text x="510" y="64" font-size="12" fill="#0F172A">Fan curve</text>
  <line x1="470" y1="80" x2="502" y2="80" stroke="#334155" stroke-width="2.5" stroke-dasharray="7 5"/>
  <text x="510" y="84" font-size="12" fill="#0F172A">System resistance</text>

  <text x="{sx(1006)}" y="{op_y-14}" font-size="12.5" fill="#E21E26" font-weight="700" text-anchor="end">Operating point &#8776; 1,000 m&#179;/h at 68 Pa</text>
  <text x="{sx(1085)}" y="{Y1-22}" font-size="12" fill="#64748B" text-anchor="start">Free air: 1,250 m&#179;/h at 0 Pa</text>
  <text x="{X0+10}" y="{sy(190)-10}" font-size="12" fill="#64748B">Shut-off: 190 Pa at zero flow</text>
  <text x="{X0+10}" y="{Y0+16}" font-size="11.5" fill="#94A3B8">Schematic &#8212; the shape is what matters, not the exact figures</text>
</svg>
</div>
<p class="tnote">Schematic of an axial fan against a typical ducted installation. The catalogue figure is the point where the red curve meets the horizontal axis; the airflow you actually get is where it meets the system curve.</p>
"""

SECTION = f"""  <h3 style="font-size:19px;color:#0F172A;margin:34px 0 12px;">The fan curve shows what the catalogue figure hides</h3>
  <p>A catalogue airflow is a single point on a curve: zero resistance, maximum flow. As resistance rises the fan moves less air, until at shut-off pressure it moves none. The installation has its own curve, and the airflow you will actually measure is where the two cross &mdash; the operating point.</p>
{SVG}
  <p>Two things follow from the shape of that chart. First, the operating point sits well below the catalogue figure even on a modest duct run &mdash; on the schematic above it is roughly 20% down, which is exactly the 10&ndash;20% loss most installations show. Second, the left-hand part of the fan curve is flat: a small increase in resistance there costs a lot of airflow, while the same increase near free air costs almost nothing. That is why a blocked filter or a half-closed shutter can halve the extract while the fan still sounds normal.</p>
  <p><strong>What to ask a supplier for.</strong> A performance table, not a headline number: airflow at 0, 50, 100 and 150 Pa for the model you are buying. Pick the model whose airflow <em>at your calculated static pressure</em> still meets the air-change target. If a supplier can only quote a free-air figure, treat that figure as a best case and size up one step for any ducted installation. Our own model tables are on the <a href="/exhaust-fan-sizes-guide" style="color:#C0392B;font-weight:700;">size guide</a>, and if airflow has already dropped on a unit in service, the <a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:700;">maintenance guide</a> covers what usually caused it.</p>
"""

p = SITE + FN
raw = open(p, "rb").read().decode("utf-8")
marker = "    <!-- MARKER_STEP5_20261020 -->"
assert raw.count(marker) == 1, "marker not unique"
raw = raw.replace(marker, SECTION + marker)

if ".tnote{" not in raw:
    TBL_CSS = """/* spec tables + chart notes */
.twrap{overflow-x:auto;margin:0 0 6px;}
.tnote{font-size:12.5px;color:#64748B;margin:8px 0 46px;line-height:1.7;}
.spec-table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;}
.spec-table th{background:#0F172A;color:#fff;padding:11px 14px;text-align:left;font-weight:700;font-size:13px;}
.spec-table td{padding:11px 14px;border-bottom:1px solid #E2E8F0;vertical-align:top;}
"""
    i = raw.find("</style>")
    raw = raw[:i] + TBL_CSS + raw[i:]
    print("CSS injected for .tnote/.twrap")

open(p, "wb").write(raw.encode("utf-8"))
print("inserted", len(SECTION), "chars; svg points", len(fan), len(sys_))
print("twrap count in page:", raw.count('class="twrap"'))
