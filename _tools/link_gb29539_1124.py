#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add internal links to new GB 29539 page + sitemap entry. Byte-level, CRLF-safe, idempotent."""
import sys
APPLY = "--apply" in sys.argv
TARGET = "/gb-29539-2025-ventilating-fan-energy-efficiency"
NL = "\r\n"

def edit(path, anchor, insertion, label, where="after"):
    with open(path, "rb") as f:
        raw = f.read()
    assert raw.count(b"\n") == raw.count(b"\r\n"), path + " not CRLF"
    text = raw.decode("utf-8")
    marker = "<!-- GB29539-LINK:" + label + " -->"
    if marker in text:
        print("SKIP", label, "(already applied)")
        return
    c = text.count(anchor)
    if c != 1:
        print("FAIL anchor count", c, "for", label); sys.exit(1)
    block = (anchor + NL + marker + NL + insertion.replace("\n", NL)) if where == "after" \
            else (marker + NL + insertion.replace("\n", NL) + NL + anchor)
    if APPLY:
        text = text.replace(anchor, block, 1)
        out = text.encode("utf-8")
        assert out.count(b"\n") == out.count(b"\r\n"), path + " CRLF broken"
        with open(path, "wb") as f:
            f.write(out)
    print("NEW ", label, "->", path)

# 1) certifications-guide Related Articles: insert a new <li> after the section opening <ul>
edit("exhaust-fan-certifications-guide.html",
     '<section class="related"><h2>Related Articles</h2><ul>',
     '<li><a href="' + TARGET + '">GB 29539-2025: China Fan Energy Efficiency Standard Explained</a></li>',
     "cert-related")

# 2) resources.html: insert a card after the IE card
edit("resources.html",
     '<article class="card"><span class="tag">Technical</span><h2>IE Motor Efficiency Classes Explained</h2><p>What IE1 to IE5 mean under IEC 60034-30-1:2025, why most small fan motors fall outside its scope, and how to verify a claim.</p><a href="/exhaust-fan-motor-efficiency-ie-classes">Open the IE efficiency guide →</a></article>',
     '<article class="card"><span class="tag">Technical</span><h2>GB 29539-2025 Energy Efficiency Standard</h2><p>China&rsquo;s mandatory 2026 fan efficiency rule: three grades, standby limits, DC fans in scope, and what it means for export buyers.</p><a href="' + TARGET + '">Open the GB 29539 guide →</a></article>',
     "resources-card")

# 3) IE page: insert a link line at the start of the "next" list
edit("exhaust-fan-motor-efficiency-ie-classes.html",
     '<h2 id="next">Specify the duty, not just the letter</h2>',
     '<p>For the Chinese domestic energy-efficiency framework and how it differs from the IE motor classes used in export markets, see the <a href="' + TARGET + '" style="color:#C0392B;font-weight:700;">GB 29539-2025 guide</a>.</p>',
     "ie-crosslink")

# 4) sitemap: insert new <url> block before </urlset>
sitemap_entry = '''  <url>
    <loc>https://baer-ventilation.com/gb-29539-2025-ventilating-fan-energy-efficiency</loc>
    <lastmod>2026-11-24</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://baer-ventilation.com/images/winding-station.webp</image:loc>
      <image:title>GB 29539-2025 energy efficiency guide - motor winding station</image:title>
    </image:image>
  </url>'''
edit("sitemap.xml", "</urlset>", sitemap_entry, "sitemap")

print("APPLIED" if APPLY else "DRY RUN")
