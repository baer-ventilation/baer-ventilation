# -*- coding: utf-8 -*-
"""
Article-driven AEO: map Google Merchant Center conversational attributes to
schema.org on the independent site (no Merchant Center feed / no prices).

P1: KLT 6 pages  -> FAQPage JSON-LD + visible FAQ + catalog PDF link
P2: KLT series   -> ProductGroup JSON-LD with variesBy + hasVariant
P3: 12 EN product pages -> Product.isSimilarTo relationship graph

Idempotent, CRLF-adaptive, byte-level. Usage:
    python _tools/conversational_attrs_1127.py --dry-run
    python _tools/conversational_attrs_1127.py
"""
import json, sys, re

DRY = '--dry-run' in sys.argv
ROOT = '.'

MODELS = {
    '10b': dict(sku='KLT-10B', inch='6-Inch', airflow='150 m³/h', watt='30 W', db='35 dB',
                panel='200×200 mm', outlet='Φ85 mm', size='6 inch', rooms='bathrooms, kitchens and small commercial rooms',
                install='160×160 mm', speed='1200 r/min', ctn='20 pcs/ctn', vol='0.108 m³'),
    '12b': dict(sku='KLT-12B', inch='8-Inch', airflow='380 m³/h', watt='30 W', db='38 dB',
                panel='250×250 mm', outlet='Φ100 mm', size='8 inch', rooms='larger bathrooms, utility rooms and small kitchens',
                install='205×205 mm', speed='1200 r/min', ctn='12 pcs/ctn', vol='0.142 m³'),
    '18b': dict(sku='KLT-18B', inch='10-Inch', airflow='432 m³/h', watt='40 W', db='42 dB',
                panel='310×310 mm', outlet='Φ100 mm', size='10 inch', rooms='commercial washrooms, kitchens and small workshops',
                install='245×245 mm', speed='1130 r/min', ctn='10 pcs/ctn', vol='0.172 m³'),
    '20b': dict(sku='KLT-20B', inch='12-Inch', airflow='792 m³/h', watt='80 W', db='45 dB',
                panel='340×340 mm', outlet='Φ100 mm', size='12 inch', rooms='workshops, canteens and mid-size commercial spaces',
                install='290×290 mm', speed='1100 r/min', ctn='8 pcs/ctn', vol='0.189 m³'),
    '25b': dict(sku='KLT-25B', inch='14-Inch', airflow='1500 m³/h', watt='120 W', db='48 dB',
                panel='400×400 mm', outlet='Φ150 mm', size='14 inch', rooms='factories, warehouses and large commercial halls',
                install='330×330 mm', speed='650 r/min', ctn='4 pcs/ctn', vol='0.157 m³'),
    '30b': dict(sku='KLT-30B', inch='18-Inch', airflow='1800 m³/h', watt='120 W', db='48 dB',
                panel='600×600 mm', outlet='Φ150 mm', size='18 inch', rooms='industrial workshops, warehouses and agricultural buildings',
                install='480×480 mm', speed='685 r/min', ctn='1 pcs/ctn', vol='0.118 m³'),
}

# P3 relationship graph: each SKU points to 2 genuinely similar siblings.
SIMILAR = {
    'product-klt-10b.html': ['product-klt-12b', 'product-klt-18b'],
    'product-klt-12b.html': ['product-klt-10b', 'product-klt-18b'],
    'product-klt-18b.html': ['product-klt-12b', 'product-klt-20b'],
    'product-klt-20b.html': ['product-klt-18b', 'product-klt-25b'],
    'product-klt-25b.html': ['product-klt-20b', 'product-klt-30b'],
    'product-klt-30b.html': ['product-klt-25b'],
    'product-6inch-984cfm.html': ['product-window-fan', 'product-ceiling-mount-fan'],
    'product-window-fan.html': ['product-6inch-984cfm', 'product-ceiling-mount-fan'],
    'product-ceiling-mount-fan.html': ['product-window-fan', 'product-6inch-984cfm'],
    'product-inline-duct-fan.html': ['product-silent-cabinet-fan'],
    'product-silent-cabinet-fan.html': ['product-inline-duct-fan', 'product-silent-bathroom-fan'],
    'product-silent-bathroom-fan.html': ['product-silent-cabinet-fan'],
}

changes = []


def crlf(s):
    """Normalise a text fragment to the file's dominant newline style."""
    return s.replace('\r\n', '\n').replace('\n', '\r\n')


def read(path):
    return open(path, 'rb').read().decode('utf-8')


def write(path, text):
    open(path, 'wb').write(text.encode('utf-8'))


def faq_for(m):
    """4 Q&A, every answer traceable to the page's own spec table / lead."""
    return [
        {"@type": "Question", "name": f"What size is the {m['sku']} and how much air does it move?",
         "acceptedAnswer": {"@type": "Answer", "text": f"The {m['sku']} is a {m['size']} square-panel wall exhaust fan delivering {m['airflow']} at {m['watt']}. It has a {m['panel']} front panel and a {m['outlet']} duct outlet, and is sized for {m['rooms']}."}},
        {"@type": "Question", "name": f"What voltage and frequency does the {m['sku']} use?",
         "acceptedAnswer": {"@type": "Answer", "text": "The standard version is 220 V / 50 Hz. A 110 V / 60 Hz version is available on OEM request. Tell us your market and we will confirm the correct electrical version before quoting."}},
        {"@type": "Question", "name": f"What is the MOQ and lead time for the {m['sku']}?",
         "acceptedAnswer": {"@type": "Answer", "text": f"MOQ is 100 pcs per model. Sample lead time is 3-7 days; a formal quotation is available within 24 hours. Packing is {m['ctn']}."}},
        {"@type": "Question", "name": f"Does the {m['sku']} include an auto shutter?",
         "acceptedAnswer": {"@type": "Answer", "text": "Yes. An integrated gravity auto-shutter closes when the fan stops, sealing the wall opening against dust, insects and back-draft. The fan mounts directly to the duct outlet without an adaptor."}},
    ]


def visible_faq(m):
    items = faq_for(m)
    rows = '\n'.join(
        '  <details><summary>%s <span>+</span></summary><div class="fa">%s</div></details>' % (q['name'], q['acceptedAnswer']['text'])
        for q in items
    )
    # Self-contained inline styles: KLT pages do not define .faqwrap/.section-tag.
    return (
        '<section class="section" style="max-width:900px;margin:0 auto;">\n'
        '  <h2 style="font-size:26px;margin:0 0 20px;">Frequently Asked Questions</h2>\n'
        '  <div style="border-top:1px solid #E2E8F0;">\n' + rows + '\n  </div>\n'
        '  <p style="margin:18px 0 0;font-size:14px;color:#64748B;">Need the full specification table? '
        '<a href="/baer-fan-catalog.pdf" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:underline;">Download the BAER catalog (PDF)</a>.</p>\n'
        '</section>\n\n'
    )


# ---------------- P1: KLT product pages ----------------
for key, m in MODELS.items():
    path = f'{ROOT}/product-klt-{key}.html'
    s = read(path)
    orig = s
    guard = 'FAQPage'

    if guard not in s:
        faq_json = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                               "mainEntity": faq_for(m)}, ensure_ascii=False)
        block = ('<script type="application/ld+json">' + faq_json + '</script>\n')
        head_anchor = crlf('</head>\n')
        assert s.count(head_anchor) == 1, f'{path}: head anchor not unique: {s.count(head_anchor)}'
        s = s.replace(head_anchor, crlf(block) + head_anchor, 1)

        foot_anchor = '<footer><div class="foot-inner">'
        assert s.count(foot_anchor) == 1, f'{path}: footer anchor not unique'
        s = s.replace(foot_anchor, crlf(visible_faq(m)) + foot_anchor, 1)

        # Catalog link in nav (mirrors the 6 template pages).
        # Locate the nav-links block, then inject only into its first Contact link.
        nav_m = re.search(r'(<div class="nav-links">)(.*?)(</div>)', s, re.S)
        assert nav_m, f'{path}: nav-links block not found'
        block = nav_m.group(0)
        contact = '<a href="/contact">Contact</a>'
        assert block.count(contact) == 1, f'{path}: Contact not unique inside nav'
        nav_new_block = block.replace(contact, contact + '<a href="/baer-fan-catalog.pdf" target="_blank">Catalog</a>', 1)
        s = s[:nav_m.start()] + nav_new_block + s[nav_m.end():]
        changes.append(f'P1 {path}: FAQPage JSON-LD + visible FAQ + catalog link')

    if s != orig:
        changes.append(f'   -> wrote {path}')
        if not DRY:
            write(path, s)

# ---------------- P2: KLT series ProductGroup ----------------
path = f'{ROOT}/klt-series-panel-exhaust-fan.html'
s = read(path)
if 'ProductGroup' not in s:
    variants = []
    for m in MODELS.values():
        variants.append({
            "@type": "Product", "name": f"{m['sku']} {m['inch']} Panel Exhaust Fan",
            "sku": m['sku'], "url": f"https://baer-ventilation.com/product-klt-{m['sku'].split('-')[1].lower()}",
            "additionalProperty": [
                {"@type": "PropertyValue", "name": "Airflow", "value": m['airflow']},
                {"@type": "PropertyValue", "name": "Power", "value": m['watt']},
                {"@type": "PropertyValue", "name": "Noise", "value": m['db']},
            ]})
    pg = {
        "@context": "https://schema.org", "@type": "ProductGroup",
        "@id": "https://baer-ventilation.com/klt-series-panel-exhaust-fan#productgroup",
        "name": "KLT Series Panel Exhaust Fan", "productGroupID": "KLT",
        "url": "https://baer-ventilation.com/klt-series-panel-exhaust-fan",
        "variesBy": ["size", "airflow", "power"], "hasVariant": variants,
    }
    block = '<script type="application/ld+json">' + json.dumps(pg, ensure_ascii=False) + '</script>\n'
    head_anchor = crlf('</head>\n')
    assert s.count(head_anchor) == 1
    s = s.replace(head_anchor, crlf(block) + head_anchor, 1)
    changes.append('P2 klt-series-panel-exhaust-fan.html: ProductGroup + variesBy + 6 variants')
    if not DRY:
        write(path, s)

# ---------------- P3: isSimilarTo on 12 EN product pages ----------------
for fn, rel in SIMILAR.items():
    path = f'{ROOT}/{fn}'
    s = read(path)
    if 'isSimilarTo' in s:
        continue
    m = re.search(r'("minimumOrderQuantity": 100)(?=[,}])', s)
    assert m, f'{fn}: min qty anchor not found'
    refs = [{"@type": "Product", "url": f"https://baer-ventilation.com/{r}"} for r in rel]
    ins = ', "isSimilarTo": ' + json.dumps(refs, ensure_ascii=False)
    s = s[:m.end()] + ins + s[m.end():]
    changes.append(f'P3 {fn}: isSimilarTo -> {rel}')
    if not DRY:
        write(path, s)

print(f'MODE: {"DRY-RUN" if DRY else "APPLY"}')
for c in changes:
    print(' ', c)
print(f'TOTAL lines: {len(changes)}')
