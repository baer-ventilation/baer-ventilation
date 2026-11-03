# -*- coding: utf-8 -*-
"""Wire the new AR kitchen page: hreflang + lang-switch on EN page, sitemap,
llms.txt, and two Arabic inbound links. Byte-level edits, CRLF preserved."""
import io, sys

ROOT = r"D:/WorkBuddy/2026-10-08-15-46-08/site"
def rd(p): return open(p, "rb").read().decode("utf-8")
def wr(p, s): open(p, "wb").write(s.encode("utf-8"))

def patch(path, pairs, label):
    s = rd(path)
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            print(f"!! {label}: expected 1 match, got {n}: {old[:70]!r}")
            sys.exit(1)
        s = s.replace(old, new)
    wr(path, s)
    print(f"ok {label}")

# 1. EN kitchen page: hreflang + lang switch
patch(ROOT + "/commercial-kitchen-exhaust-fans.html", [(
 '<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">',
 '<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">\r\n'
 '<link rel="alternate" hreflang="ar" href="https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans">\r\n'
 '<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">'
)], "en hreflang")

patch(ROOT + "/commercial-kitchen-exhaust-fans.html", [(
 '<div class="lang-switch">\r\n      <a href="/commercial-kitchen-exhaust-fans" class="active">EN</a>\r\n    </div>',
 '<div class="lang-switch">\r\n      <a href="/commercial-kitchen-exhaust-fans" class="active">EN</a>\r\n'
 '      <a href="/ar/commercial-kitchen-exhaust-fans">\u0627\u0644\u0639\u0631\u0628\u064a\u0629</a>\r\n    </div>'
)], "en lang-switch")

# 2. sitemap
patch(ROOT + "/sitemap.xml", [(
 '    <loc>https://baer-ventilation.com/ar/product-inline-duct-fan</loc>\r\n'
 '    <lastmod>2026-11-02</lastmod>',
 '    <loc>https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans</loc>\r\n'
 '    <lastmod>2026-11-03</lastmod>\r\n'
 '    <changefreq>monthly</changefreq>\r\n'
 '  </url>\r\n'
 '  <url>\r\n'
 '    <loc>https://baer-ventilation.com/ar/product-inline-duct-fan</loc>\r\n'
 '    <lastmod>2026-11-02</lastmod>'
)], "sitemap")

# 3. llms.txt Arabic block
patch(ROOT + "/llms.txt", [(
 '[Saudi Arabia supplier (Arabic)](https://baer-ventilation.com/ar/saudi-arabia-exhaust-fan-supplier)',
 '[Saudi Arabia supplier (Arabic)](https://baer-ventilation.com/ar/saudi-arabia-exhaust-fan-supplier)'
 ' \u00b7 [Commercial kitchen exhaust fans (Arabic)](https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans)'
)], "llms.txt")

# 4. AR product page: fourth application card linking to the guide
patch(ROOT + "/ar/product-inline-duct-fan.html", [(
 '<div class="appcard"><h4>\u062a\u0639\u0632\u064a\u0632 \u0627\u0644\u0645\u062c\u0627\u0631\u064a \u0627\u0644\u0637\u0648\u064a\u0644\u0629</h4><p>\u0631\u0641\u0639 \u062a\u062f\u0641\u0642 \u0627\u0644\u0647\u0648\u0627\u0621 \u0641\u064a \u0623\u0646\u0638\u0645\u0629 \u0627\u0644\u0642\u0646\u0648\u0627\u062a \u0627\u0644\u0637\u0648\u064a\u0644\u0629 \u0623\u0648 \u0627\u0644\u0645\u0639\u0642\u062f\u0629.</p></div>',
 '<div class="appcard"><h4>\u062a\u0639\u0632\u064a\u0632 \u0627\u0644\u0645\u062c\u0627\u0631\u064a \u0627\u0644\u0637\u0648\u064a\u0644\u0629</h4><p>\u0631\u0641\u0639 \u062a\u062f\u0641\u0642 \u0627\u0644\u0647\u0648\u0627\u0621 \u0641\u064a \u0623\u0646\u0638\u0645\u0629 \u0627\u0644\u0642\u0646\u0648\u0627\u062a \u0627\u0644\u0637\u0648\u064a\u0644\u0629 \u0623\u0648 \u0627\u0644\u0645\u0639\u0642\u062f\u0629.</p></div>\r\n'
 '      <div class="appcard"><h4>\u0637\u0631\u062f \u0645\u0637\u0627\u0628\u062e \u0627\u0644\u0645\u0637\u0627\u0639\u0645 \u0648\u0627\u0644\u0645\u0642\u0627\u0647\u064a</h4><p>\u062a\u062d\u062c\u064a\u0645 \u0627\u0644\u0637\u0631\u062f \u0648\u0647\u0648\u0627\u0621 \u0627\u0644\u062a\u0639\u0648\u064a\u0636 \u0648\u0633\u0631\u0639\u0629 \u0627\u0644\u0642\u0646\u0627\u0629 \u0648\u0645\u064a\u0632\u0627\u0646\u064a\u0629 \u0627\u0644\u0636\u063a\u0637 \u2014 \u0631\u0627\u062c\u0639 <a href="https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans" style="color:#C0392B;font-weight:600;">\u062f\u0644\u064a\u0644 \u0645\u0631\u0627\u0648\u062d \u0639\u0627\u062f\u0645 \u0627\u0644\u0645\u0637\u0627\u0628\u062e \u0627\u0644\u062a\u062c\u0627\u0631\u064a\u0629</a>.</p></div>'
)], "ar product appcard")

# 5. ar/products card description link
patch(ROOT + "/ar/products/index.html", [(
 '<p>\u0645\u0631\u0627\u0648\u062d \u0642\u0646\u0648\u0627\u062a \u0644\u0627\u0633\u062a\u0631\u062f\u0627\u062f \u0627\u0644\u062d\u0631\u0627\u0631\u0629 \u0648\u0627\u0644\u062a\u0643\u064a\u064a\u0641 \u0648\u0627\u0644\u0645\u062c\u0627\u0631\u064a \u0627\u0644\u0637\u0648\u064a\u0644\u0629 \u2014 AC \u0648DC.</p>',
 '<p>\u0645\u0631\u0627\u0648\u062d \u0642\u0646\u0648\u0627\u062a \u0644\u0627\u0633\u062a\u0631\u062f\u0627\u062f \u0627\u0644\u062d\u0631\u0627\u0631\u0629 \u0648\u0627\u0644\u062a\u0643\u064a\u064a\u0641 \u0648\u0627\u0644\u0645\u062c\u0627\u0631\u064a \u0627\u0644\u0637\u0648\u064a\u0644\u0629 \u2014 AC \u0648DC. '
 '\u0648\u0644\u062a\u0637\u0628\u064a\u0642\u0627\u062a \u0645\u0637\u0627\u0628\u062e \u0627\u0644\u0645\u0637\u0627\u0639\u0645 \u0631\u0627\u062c\u0639 <a href="https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans" style="color:#C0392B;font-weight:600;">\u062f\u0644\u064a\u0644 \u0639\u0627\u062f\u0645 \u0627\u0644\u0645\u0637\u0627\u0628\u062e \u0627\u0644\u062a\u062c\u0627\u0631\u064a\u0629</a>.</p>'
)], "ar products card")
