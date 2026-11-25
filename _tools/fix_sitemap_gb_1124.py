#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the GB 29539 <url> block inside </urlset> (was appended after root)."""
import sys
PATH = "sitemap.xml"
APPLY = "--apply" in sys.argv
with open(PATH, "rb") as f:
    raw = f.read()
assert raw.count(b"\n") == raw.count(b"\r\n")
text = raw.decode("utf-8")
NL = "\r\n"
bad = '</urlset>' + NL + '<!-- GB29539-LINK:sitemap -->' + NL + \
'''  <url>
    <loc>https://baer-ventilation.com/gb-29539-2025-ventilating-fan-energy-efficiency</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://baer-ventilation.com/images/winding-station.webp</image:loc>
      <image:title>GB 29539-2025 energy efficiency guide - motor winding station</image:title>
    </image:image>
  </url>'''.replace("\n", NL)
good = '<!-- GB29539-LINK:sitemap -->' + NL + \
'''  <url>
    <loc>https://baer-ventilation.com/gb-29539-2025-ventilating-fan-energy-efficiency</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://baer-ventilation.com/images/winding-station.webp</image:loc>
      <image:title>GB 29539-2025 energy efficiency guide - motor winding station</image:title>
    </image:image>
  </url>'''.replace("\n", NL) + NL + '</urlset>'
assert text.count(bad) == 1, text.count(bad)
if not APPLY:
    print("DRY RUN: will move GB url block inside </urlset>")
    sys.exit(0)
text = text.replace(bad, good, 1)
out = text.encode("utf-8")
assert out.count(b"\n") == out.count(b"\r\n")
with open(PATH, "wb") as f:
    f.write(out)
print("FIXED")
