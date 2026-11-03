# -*- coding: utf-8 -*-
"""Wire the new maintenance guide into sitemap, llms.txt and 5 inbound-link spots."""
import re

SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"
SLUG = "exhaust-fan-maintenance-guide"

def load(fn):
    return open(SITE + fn, "rb").read().decode("utf-8")

def save(fn, s):
    open(SITE + fn, "wb").write(s.encode("utf-8"))

def eol(s):
    return "\r\n" if "\r\n" in s else "\n"

def rep(fn, old, new, label):
    s = load(fn)
    c = s.count(old)
    if c != 1:
        print(f"  !! {fn} [{label}] matches={c} -- SKIP")
        return
    save(fn, s.replace(old, new))
    print(f"  ok {fn} [{label}]")

# 1) sitemap
s = load("sitemap.xml")
E = eol(s)
newurl = (f'  <url>{E}'
          f'    <loc>https://baer-ventilation.com/{SLUG}</loc>{E}'
          f'    <lastmod>2026-11-03</lastmod>{E}'
          f'    <changefreq>monthly</changefreq>{E}'
          f'    <priority>0.8</priority>{E}'
          f'  </url>{E}')
if SLUG in s:
    print("  skip sitemap: already present")
else:
    save("sitemap.xml", s.replace("</urlset>", newurl + "</urlset>"))
    print("  ok sitemap.xml (+1 url)")

# 2) llms.txt
s = load("llms.txt")
E = eol(s)
line = (f"- [Exhaust Fan Maintenance Guide](https://baer-ventilation.com/{SLUG}): what fails first "
        f"(capacitor, blade fouling, shutter mechanism), a 12-month cleaning schedule by environment, "
        f"electrical checks, spare parts to hold, and repair-or-replace rules.{E}")
if SLUG in s:
    print("  skip llms.txt: already present")
else:
    anchor = "- [Industrial Exhaust Fans](https://baer-ventilation.com/industrial-exhaust-fans)"
    i = s.find(anchor)
    j = s.find(E, i) + len(E)
    save("llms.txt", s[:j] + line + s[j:])
    print("  ok llms.txt (+1 entry)")

# 3) exhaust-fans hub: sentence link
rep("exhaust-fans.html",
    "Dust on the impeller silently cuts airflow; a twice-yearly clean restores performance.",
    'Dust on the impeller silently cuts airflow; a twice-yearly clean restores performance &mdash; the '
    '<a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:700;">maintenance guide</a> sets the interval for each environment.',
    "sentence")

# 4) exhaust-fans hub: related list entry after noise guide
rep("exhaust-fans.html",
    '<li><a href="/exhaust-fan-noise-levels-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">Exhaust Fan Noise Levels Guide</a></li>',
    '<li><a href="/exhaust-fan-noise-levels-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">Exhaust Fan Noise Levels Guide</a></li>\n'
    '<li><a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">Exhaust Fan Maintenance Guide</a></li>',
    "related-list")

# 5) installation guide
rep("panel-exhaust-fan-installation-guide.html",
    "add a cleaning interval to the maintenance schedule",
    'add a cleaning interval to the <a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:600;">12-month maintenance schedule</a>',
    "table-cell")

# 6) shutter types
rep("exhaust-fan-shutter-types.html",
    "A shutter that stays open is almost always a dirty pin, not a broken blade.",
    'A shutter that stays open is almost always a dirty pin, not a broken blade. The full service routine is in the '
    '<a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:600;">exhaust fan maintenance guide</a>.',
    "bullet")

# 7) kitchen page
rep("commercial-kitchen-exhaust-fans.html",
    "an impeller that gets washed every season",
    'an impeller that gets washed every season (the '
    '<a href="/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:600;">maintenance schedule</a> sets the interval by grease load)',
    "grease-note")

print("done")
