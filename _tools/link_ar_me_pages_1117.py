#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ar 中东三页收尾：EN 页 hreflang 对称 + ar 页互链改 ar 版 + sitemap +3 条。dry-run 默认，--apply 落盘。"""
import sys

APPLY = "--apply" in sys.argv

def load(p):
    b = open(p, "rb").read()
    return b, b.decode("utf-8")

def save(p, s, nl):
    open(p, "wb").write(s.replace("\n", nl).encode("utf-8"))

def edit(path, fn, label):
    raw, s = load(path)
    nl = "\r\n" if "\r\n" in s else "\n"
    new, n = fn(s, nl)
    if n == 0:
        print(f"SKIP  {path} ({label}) - no change")
        return
    print(f"{'APPLY' if APPLY else 'DRY  '}  {path:48s} +{n} 处")
    if APPLY:
        save(path, new, nl)

# ---------- 1) EN 三页：canonical 后插 hreflang 三件套 ----------
def add_hreflang(slug):
    def fn(s, nl):
        if 'hreflang="ar"' in s:
            return s, 0
        anchor = f'<link rel="canonical" href="https://baer-ventilation.com/{slug}">'
        assert s.count(anchor) == 1
        block = (f'<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/{slug}">{nl}'
                 f'<link rel="alternate" hreflang="ar" href="https://baer-ventilation.com/ar/{slug}">{nl}'
                 f'<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/{slug}">')
        return s.replace(anchor, anchor + nl + block), 3
    return fn

edit("uae-exhaust-fan-supplier.html", add_hreflang("uae-exhaust-fan-supplier"), "hreflang x3")
edit("iraq-exhaust-fan-supplier.html", add_hreflang("iraq-exhaust-fan-supplier"), "hreflang x3")
edit("middle-east-exhaust-fan-supplier.html", add_hreflang("middle-east-exhaust-fan-supplier"), "hreflang x3")

# ---------- 2) ar/saudi：3 张卡片链改 ar 版 ----------
def fix_saudi(s, nl):
    n = 0
    pairs = [
        ('<a href="../uae-exhaust-fan-supplier">صفحة الإمارات (إنجليزي) ←</a>',
         '<a href="uae-exhaust-fan-supplier">الصفحة الإماراتية (عربي) ←</a>'),
        ('<a href="../iraq-exhaust-fan-supplier">صفحة العراق (إنجليزي) ←</a>',
         '<a href="iraq-exhaust-fan-supplier">الصفحة العراقية (عربي) ←</a>'),
        ('<a href="../middle-east-exhaust-fan-supplier">المركز الرئيسي (إنجليزي) ←</a>',
         '<a href="middle-east-exhaust-fan-supplier">المركز الرئيسي (عربي) ←</a>'),
    ]
    for a, b in pairs:
        assert s.count(a) == 1, a
        s = s.replace(a, b); n += 1
    return s, n

edit("ar/saudi-arabia-exhaust-fan-supplier.html", fix_saudi, "卡片链改 ar 版 x3")

# ---------- 3) ar/index：uae/hub 改 ar 版 + 插入 iraq 卡片 ----------
def fix_index(s, nl):
    if 'href="iraq-exhaust-fan-supplier"' in s:
        return s, 0
    n = 0
    reps = [
        ('<a href="../uae-exhaust-fan-supplier">صفحة الإمارات (إنجليزي) ←</a>',
         '<a href="uae-exhaust-fan-supplier">صفحة السوق الإماراتي ←</a>'),
        ('<a href="../middle-east-exhaust-fan-supplier">نظرة عامة (إنجليزي) ←</a>',
         '<a href="middle-east-exhaust-fan-supplier">نظرة عامة على الشرق الأوسط ←</a>'),
    ]
    for a, b in reps:
        assert s.count(a) == 1, a
        s = s.replace(a, b); n += 1
    # 在 uae 卡片 </div> 后插入 iraq 卡片
    uae_end = s.find('صفحة السوق الإماراتي ←</a>\n        </div>') + len('صفحة السوق الإماراتي ←</a>\n        </div>')
    iraq_card = (f'{nl}        <div class="card">{nl}'
                 f'            <h3>العراق</h3>{nl}'
                 f'            <p>مراوح بمحركات جهد واسع 180–250 فولت لشبكة متقلبة، مقاومة للغبار وحرارة 50°م.</p>{nl}'
                 f'            <a href="iraq-exhaust-fan-supplier">صفحة السوق العراقي ←</a>{nl}'
                 f'        </div>')
    s = s[:uae_end] + iraq_card + s[uae_end:]
    return s, n + 1

edit("ar/index.html", fix_index, "uae/hub 改 ar + 插 iraq 卡")

# ---------- 4) sitemap +3 条 ar URL ----------
def fix_sitemap(s, nl):
    added = 0
    slugs = [("ar/uae-exhaust-fan-supplier", "ceiling-fan-product.webp", "Exhaust fan supplier page for the UAE (Arabic)"),
             ("ar/iraq-exhaust-fan-supplier", "warehouse-cartons.webp", "Exhaust fan supplier page for Iraq (Arabic)"),
             ("ar/middle-east-exhaust-fan-supplier", "baer-gate-stone.webp", "Middle East exhaust fan manufacturer hub (Arabic)")]
    for slug, img, ttl in slugs:
        url = f"https://baer-ventilation.com/{slug}"
        if url in s:
            continue
        block = (f'  <url>\n    <loc>{url}</loc>\n    <lastmod>2026-11-17</lastmod>\n'
                 f'    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n'
                 f'    <image:image>\n      <image:loc>https://baer-ventilation.com/images/{img}</image:loc>\n'
                 f'      <image:title>{ttl}</image:title>\n    </image:image>\n  </url>\n')
        assert s.count('</urlset>') == 1
        s = s.replace('</urlset>', block + '</urlset>')
        added += 1
    return s, added

edit("sitemap.xml", fix_sitemap, "sitemap +3 ar URL")

print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'} done")
