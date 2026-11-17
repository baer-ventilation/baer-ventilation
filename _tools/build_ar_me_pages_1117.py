#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ar 版中东落地页构建器：uae / iraq / middle-east 枢纽。
样板（CSS/topbar/header/footer/GA）从 ar/saudi 页自动提取，正文由 ar_*_content 模块提供。
用法：python build_ar_me_pages_1117.py [--apply]
"""
import sys, importlib

APPLY = "--apply" in sys.argv
TPL = open("ar/saudi-arabia-exhaust-fan-supplier.html", encoding="utf-8").read().replace("\r\n", "\n")

def between(s, a, b):
    i = s.find(a)
    assert i >= 0, a
    j = s.find(b, i)
    return s[i:j + len(b)]

CSS_MAIN = between(TPL, "<style>", "</style>")            # 主样式（含 kv/tbl/cards/tip/faq/cta-box）
TB_CSS   = between(TPL, "<style>/* bv-topbar */", "</style>")
CLARITY  = between(TPL, "<!-- Microsoft Clarity -->", "</script>")
TOPBAR   = between(TPL, '<div class="bv-topbar">', "\n\n<header class=\"header\">")
HEADER   = between(TPL, '<header class="header">', "</header>")
FOOTER   = between(TPL, '<footer class="footer">', "</footer>")
GA       = between(TPL, "<!-- GA4 conversion", "<script src=\"/js/reveal.js?v=1\" defer></script>")
WEBPAGE_LD = between(TPL, '"@type": "WebPage"', '"dateModified": "2026-10-22"\n}')

def build_page(c):
    """c = 内容 dict（见 ar_uae_content.py 等的注释约定）"""
    head = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y7GNF2D0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-0Y7GNF2D0H');
</script>
<title>{c['title']}</title>
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="https://baer-ventilation.com/ar/{c['slug']}">
<link rel="alternate" hreflang="ar" href="https://baer-ventilation.com/ar/{c['slug']}">
<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/{c['en_slug']}">
<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/{c['en_slug']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BAER Ventilation">
<meta property="og:locale" content="ar_SA">
<meta property="og:title" content="{c['og_title']}">
<meta property="og:description" content="{c['og_desc']}">
<meta property="og:url" content="https://baer-ventilation.com/ar/{c['slug']}">
<meta property="og:image" content="https://baer-ventilation.com/images/{c['og_img']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c['og_title']}">
<meta name="twitter:description" content="{c['og_desc']}">
<meta name="twitter:image" content="https://baer-ventilation.com/images/{c['og_img']}">
<meta name="theme-color" content="#0F172A">
<meta name="description" content="{c['og_desc']}">
<meta name="keywords" content="{c['kw']}">
{CSS_MAIN}
<script type="application/ld+json">
{c['faq_json']}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "{c['webpage_name']}",
  "description": "{c['og_desc']}",
  "url": "https://baer-ventilation.com/ar/{c['slug']}",
  "inLanguage": "ar",
  "isPartOf": {{
    "@id": "https://baer-ventilation.com/#website"
  }},
  "about": {{
    "@type": "Organization",
    "@id": "https://baer-ventilation.com/#organization",
    "name": "BAER Ventilation",
    "legalName": "Zhejiang Baer Electrical Technology Co.,ltd",
    "sameAs": [
      "https://www.youtube.com/@BAERVentilation",
      "https://www.linkedin.com/company/baer-ventilation",
      "https://discovery.patsnap.com/company/zhejiang-baer-electrical-technology",
      "https://www.qixin.com/company/46a65271-58ea-4791-bc97-10681bc264f6",
      "https://www.tradewheel.com/co/zhejiang-baer-appliance-technology-co-1040399",
      "https://www.made-in-china.com/showroom/907205f756d754e7",
      "https://www.crunchbase.com/organization/baer-ventilation",
      "https://www.wikidata.org/wiki/Q141684694",
      "https://www.facebook.com/profile.php?id=100072975690826",
      "https://www.instagram.com/ventilation_exhaustfan/"
    ],
    "url": "https://baer-ventilation.com/"
  }},
  "breadcrumb": {{
    "@id": "https://baer-ventilation.com/ar/{c['slug']}#breadcrumb"
  }},
  "dateModified": "{c['date_modified']}"
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "@id": "https://baer-ventilation.com/ar/{c['slug']}#breadcrumb",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "الرئيسية",
      "item": "https://baer-ventilation.com/ar/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{c['webpage_name']}",
      "item": "https://baer-ventilation.com/ar/{c['slug']}"
    }}
  ]
}}
</script>
{CLARITY}
{TB_CSS}
</head>
<body>

{TOPBAR}

{HEADER.replace('../saudi-arabia-exhaust-fan-supplier', '../' + c['en_slug'])}

<div class="hero">
  <div class="crumb"><a href="./">الرئيسية</a> › <span>{c['crumb']}</span></div>
  <h1>{c['h1']}</h1>
  <p>{c['hero_p']}</p>
  <p class="updated">آخر تحديث: 17 نوفمبر 2026</p>
</div>

<div class="body">

{c['body_html']}

</div>

{FOOTER}

{GA}</body>
</html>
"""
    return head

mods = ["ar_uae_content", "ar_irq_content", "ar_hub_content"]
n = 0
for m in mods:
    c = importlib.import_module(m).C
    html = build_page(c)
    tag = "APPLY" if APPLY else "DRY  "
    print(f"{tag} ar/{c['slug']}.html  bytes={len(html.encode('utf-8'))}")
    # 结构自检
    assert html.count("<h1") == 1
    assert html.count("</html>") == 1
    for t in ["div", "table", "ul", "li", "details", "dl"]:
        o = html.count("<" + t); cl = html.count("</" + t + ">")
        # <div> 无属性写法在正文里可能出现 <div class=...>，用 <div 统计
        o = html.count("<" + t + " ") + html.count("<" + t + ">")
        assert o == cl, (m, t, o, cl)
    import json, re
    for mm in re.finditer(r'<script type="application/ld\+json">\n(.*?)\n</script>', html, re.S):
        json.loads(mm.group(1))
    if APPLY:
        out = html.replace("\n", "\r\n")
        open(f"ar/{c['slug']}.html", "wb").write(out.encode("utf-8"))
        n += 1
print(f"{'APPLIED' if APPLY else 'DRY-RUN'}: {n} files")
