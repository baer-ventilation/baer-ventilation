# -*- coding: utf-8 -*-
"""Unify all BAER-owned MOQ figures to 100 pcs (Olivia 2026-11-25 decision).
Rewrites "stock 100 / OEM 500" two-tier sentences into single 100pcs statements
(no "100 stock / 100 OEM" tautology). Keeps industry-generic "100-500 pcs" ranges
(non-BAER), and unrelated 500 (airflow 500m3/h, 1500-2000 fpm, 500V, carton counts).
Byte-level, preserves CRLF. Dry-run prints hit counts; apply asserts exact hits.
"""
import sys
from collections import defaultdict

DRY = "--dry-run" in sys.argv

# Each pair is (old, new) applied across ALL scanned files globally.
# Keys chosen long/unique enough to avoid collateral damage.
RULES = [
    # ===== EN: two-tier "100 stock + 500 OEM" -> single 100 =====
    ("BAER's standard MOQ is <strong>100 pcs per model</strong> for stock exhaust fans and <strong>500 pcs per model</strong> for OEM or customised production.",
     "BAER's MOQ is <strong>100 pcs per model</strong> for both stock and OEM/customised production."),
    ("BAER's standard MOQ is <strong>100 pcs per model</strong> for stock models and <strong>500 pcs</strong> for OEM/custom, with mixed models accepted in one container.",
     "BAER's MOQ is <strong>100 pcs per model</strong> for both stock and OEM/custom, with mixed models accepted in one container."),
    ("100 pcs per model for stock models and 500 pcs for OEM/custom, with mixed models in one container accepted.",
     "100 pcs per model for both stock and OEM/custom, with mixed models in one container accepted."),
    ("MOQ is 100 pcs per model for stock models and 500 pcs for OEM/custom, with mixed models in one container accepted.",
     "MOQ is 100 pcs per model for both stock and OEM/custom, with mixed models in one container accepted."),
    ("MOQ is 100 pcs per model for stock models and 500 pcs for OEM/private-label, with mixed models accepted in one container.",
     "MOQ is 100 pcs per model for both stock and OEM/private-label, with mixed models accepted in one container."),
    ("Standard stock models: MOQ 100 pcs. OEM/custom models: MOQ 500 pcs.",
     "MOQ 100 pcs per model for both stock and OEM/custom."),
    ("the stock MOQ is 100 pcs per model and the OEM MOQ is 500 pcs per model, with different models allowed to share one container.",
     "the MOQ is 100 pcs per model for both stock and OEM, with different models allowed to share one container."),
    ("MOQ 100 pcs per model for stock versions and 500 pcs per model for OEM customisation, with mixed models allowed in one container.",
     "MOQ 100 pcs per model for both stock and OEM customisation, with mixed models allowed in one container."),
    ("100 pcs stock models / 500 pcs OEM per model",
     "100 pcs per model (stock and OEM)"),
    ("100 pcs stock / 500 pcs OEM per model",
     "100 pcs per model (stock and OEM)"),
    ("Stock models: 100 pcs, shipping from inventory. OEM with your branding: 500 pcs per model, bulk production 25&ndash;35 days from deposit and confirmed artwork.",
     "MOQ 100 pcs per model for both stock and OEM, bulk production 25&ndash;35 days from deposit and confirmed artwork."),
    ("100 pcs for stock models, 500 pcs for OEM/custom. Mixed models can share one container.",
     "100 pcs per model for stock and OEM/custom. Mixed models can share one container."),
    ("100 pcs for stock models, 500 pcs for OEM/custom. Mixed models can share one container.",
     "100 pcs per model for stock and OEM/custom. Mixed models can share one container."),
    ("Minimum OEM order is 500 pcs.",
     "Minimum order is 100 pcs."),
    ("Stock models: MOQ 100 pcs, ships in 3-7 days. OEM orders: MOQ 500 pcs, production in 25\u201335 days.",
     "MOQ 100 pcs per model, ships in 3-7 days; OEM production in 25\u201335 days."),
    ("Stock models: MOQ 100 pcs. OEM with custom logo: MOQ 500 pcs.",
     "MOQ 100 pcs per model for stock and OEM with custom logo."),
    ("MOQ 500 pcs for OEM branding, with custom colour and packaging options.",
     "MOQ 100 pcs for OEM branding, with custom colour and packaging options."),
    ("MOQ 500 pcs for custom builds, samples in 3\u20137 days.",
     "MOQ 100 pcs for custom builds, samples in 3\u20137 days."),
    ("500 pcs per model for OEM with custom branding, higher for a new mould.",
     "MOQ 100 pcs for OEM with custom branding, higher for a new mould."),
    ("MOQ:</strong> 500 pcs per model for OEM with branding; higher for a new mould.",
     "MOQ:</strong> 100 pcs per model for OEM with branding; higher for a new mould."),
    ("Custom voltage (110V, 380V three-phase) available on request with MOQ 500 pcs.",
     "Custom voltage (110V, 380V three-phase) available on request with MOQ 100 pcs."),
    ("500 pcs per model for logo printing, custom cartons and barcodes",
     "from 100 pcs per model for logo printing, custom cartons and barcodes"),
    ("500 pcs per model for logo printing, custom cartons, manuals and barcodes",
     "from 100 pcs per model for logo printing, custom cartons, manuals and barcodes"),
    ("barcodes from 500 pcs per model</li>",
     "barcodes from 100 pcs per model</li>"),
    ("typically from 500 pcs per model.",
     "typically from 100 pcs per model."),
    ("MOQ from 500 pcs per model.",
     "MOQ 100 pcs per model."),
    ("all available at MOQ from 500 pcs per model.",
     "all available at MOQ 100 pcs per model."),
    ("Your brand on the housing and carton, from 500 pcs per model.",
     "Your brand on the housing and carton, from 100 pcs per model."),
    ("<td>500 pcs (OEM)</td>",
     "<td>100 pcs</td>"),
    ("<td>500 pcs per model</td><td>Includes branding and configuration changes</td>",
     "<td>100 pcs per model</td><td>Includes branding and configuration changes</td>"),
    ("- Standard MOQ: 100 pcs (stock models) \u00b7 500 pcs (OEM/custom)",
     "- Standard MOQ: 100 pcs per model"),
    ("MOQ <span>500pcs</span>",
     "MOQ <span>100pcs</span>"),
    (">500<span style=\"font-size:14px;\">pcs</span>",
     ">100<span style=\"font-size:14px;\">pcs</span>"),

    # faq.html:445 static FAQ with <strong> tags
    ("Standard stock models: <strong>MOQ 100 pcs</strong>. OEM/custom models: <strong>MOQ 500 pcs</strong>.",
     "MOQ <strong>100 pcs per model</strong> for both stock and OEM/custom."),
    # ===== AR: two-tier -> single 100 =====
    ("\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648500 \u0642\u0637\u0639\u0629 \u0644\u0640 OEM/\u0627\u0644\u0645\u062e\u0635\u0635",
     "\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM/\u0627\u0644\u0645\u062e\u0635\u0635"),
    ("100 \u0642\u0637\u0639\u0629 \u0644\u0644\u0637\u0631\u0627\u0632\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629\u060c \u0648500 \u0642\u0637\u0639\u0629 \u0644\u0640 OEM/\u0627\u0644\u0645\u062e\u0635\u0635",
     "100 \u0642\u0637\u0639\u0629 \u0644\u0644\u0637\u0631\u0627\u0632\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM/\u0627\u0644\u0645\u062e\u0635\u0635"),
    ("100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629\u060c \u0648500 \u0642\u0637\u0639\u0629 \u0644\u0640 OEM/\u0627\u0644\u0645\u062e\u0635\u0635",
     "100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM/\u0627\u0644\u0645\u062e\u0635\u0635"),
    ("\u0627\u0644\u0646\u0645\u0627\u0630\u062c \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629: 100 \u0642\u0637\u0639\u0629. \u0646\u0645\u0627\u0630\u062c OEM \u0627\u0644\u0645\u062e\u0635\u0635\u0629: 500 \u0642\u0637\u0639\u0629.",
     "MOQ 100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0646\u0645\u0627\u0630\u062c \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM."),
    ("\u0627\u0644\u0637\u0631\u0632 \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629: MOQ 100 \u0642\u0637\u0639\u0629\u060c \u0634\u062d\u0646 \u062e\u0644\u0627\u0644 3-7 \u0623\u064a\u0627\u0645. \u0637\u0644\u0628\u0627\u062a OEM: MOQ 500 \u0642\u0637\u0639\u0629\u060c \u0625\u0646\u062a\u0627\u062c \u062e\u0644\u0627\u0644 25-35 \u064a\u0648\u0645\u064b\u0627.",
     "MOQ 100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632\u060c \u0634\u062d\u0646 \u062e\u0644\u0627\u0644 3-7 \u0623\u064a\u0627\u0645\u060c \u0648\u0625\u0646\u062a\u0627\u062c OEM \u062e\u0644\u0627\u0644 25-35 \u064a\u0648\u0645\u064b\u0627."),
    ("\u0646\u0639\u0645. \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 \u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0639\u0644\u0627\u0645\u0629 \u0627\u0644\u062a\u062c\u0627\u0631\u064a\u0629 OEM \u0647\u0648 500 \u0642\u0637\u0639\u0629",
     "\u0646\u0639\u0645. \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 100 \u0642\u0637\u0639\u0629 \u0644\u0637\u0644\u0628\u0627\u062a OEM \u0628\u0627\u0644\u0639\u0644\u0627\u0645\u0629 \u0627\u0644\u062a\u062c\u0627\u0631\u064a\u0629"),
    ("OEM \u0628\u0634\u0639\u0627\u0631 \u0645\u062e\u0635\u0635: MOQ 500 \u0642\u0637\u0639\u0629.",
     "MOQ 100 \u0642\u0637\u0639\u0629 \u0644\u0644\u0637\u0631\u0627\u0632\u0627\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM \u0628\u0634\u0639\u0627\u0631 \u0645\u062e\u0635\u0635."),
    ("<td>500 \u0642\u0637\u0639\u0629 (OEM)</td>", "<td>100 \u0642\u0637\u0639\u0629</td>"),

    # ===== ZH: two-tier -> single 100 =====
    ("\u73b0\u8d27\u578b\u53f7\uff1aMOQ 100\u53f0\uff0c3-7\u5929\u53d1\u8d27\u3002OEM\u8ba2\u5355\uff1aMOQ 500\u53f0\uff0c\u751f\u4ea7\u5468\u671f25-35\u5929\u3002",
     "MOQ 100\u53f0\uff0c3-7\u5929\u53d1\u8d27\uff1bOEM\u751f\u4ea7\u5468\u671f25-35\u5929\u3002"),
    ("OEM\u5b9a\u5236MOQ 500\u53f0\u8d77", "OEM\u5b9a\u5236MOQ 100\u53f0\u8d77"),
    ("\u73b0\u8d27\u578b\u53f7\uff1aMOQ 100\u53f0\u3002OEM\u8d34\u724c\uff1aMOQ 500\u53f0\u3002",
     "MOQ 100\u53f0\uff0c\u73b0\u8d27\u4e0eOEM\u8d34\u724c\u5747\u9002\u7528\u3002"),
    ("<td>500 \u53f0\uff08OEM\uff09</td>", "<td>100 \u53f0</td>"),

    # ===== js/main.js i18n dictionaries: specs table + why-2d + faq-a1 =====
    ("['MOQ','500 pcs']]", "['MOQ','100 pcs']]"),
    ("['MOQ','500 \u0642\u0637\u0639\u0629']]", "['MOQ','100 \u0642\u0637\u0639\u0629']]"),
    ("['MOQ','500\u4ef6\u8d77\u8ba2']]", "['MOQ','100\u4ef6\u8d77\u8ba2']]"),
    ("Custom logo, color, voltage, blade design, and packaging. MOQ from 500 pcs. Full private-label solutions available.",
     "Custom logo, color, voltage, blade design, and packaging. MOQ 100 pcs. Full private-label solutions available."),
    ("\u0634\u0639\u0627\u0631 \u0645\u062e\u0635\u0635\u060c \u0623\u0644\u0648\u0627\u0646\u060c \u062c\u0647\u062f\u060c \u062a\u0635\u0645\u064a\u0645 \u0634\u0641\u0631\u0629\u060c \u0648\u062a\u063a\u0644\u064a\u0641. \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 \u0644\u0644\u0637\u0644\u0628 500 \u0642\u0637\u0639\u0629.",
     "\u0634\u0639\u0627\u0631 \u0645\u062e\u0635\u0635\u060c \u0623\u0644\u0648\u0627\u0646\u060c \u062c\u0647\u062f\u060c \u062a\u0635\u0645\u064a\u0645 \u0634\u0641\u0631\u0629\u060c \u0648\u062a\u063a\u0644\u064a\u0641. \u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649 100 \u0642\u0637\u0639\u0629."),
    ("\u5b9a\u5236Logo\u3001\u989c\u8272\u3001\u7535\u538b\u3001\u53f6\u8f6e\u8bbe\u8ba1\u548c\u5305\u88c5\uff0c\u8d77\u8ba2\u91cf500\u4ef6\uff0c\u652f\u6301\u5168\u5957\u8d34\u724c\u670d\u52a1\u3002",
     "\u5b9a\u5236Logo\u3001\u989c\u8272\u3001\u7535\u538b\u3001\u53f6\u8f6e\u8bbe\u8ba1\u548c\u5305\u88c5\uff0c\u8d77\u8ba2\u91cf100\u4ef6\uff0c\u652f\u6301\u5168\u5957\u8d34\u724c\u670d\u52a1\u3002"),
    ("'faq-a1': 'Standard stock models: MOQ 100 pcs. OEM/custom models: MOQ 500 pcs. Flexible for first orders.'",
     "'faq-a1': 'MOQ 100 pcs per model for both stock and OEM/custom. Flexible for first orders.'"),
    ("'faq-a1': '\u0627\u0644\u0646\u0645\u0627\u0630\u062c \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629: 100 \u0642\u0637\u0639\u0629. \u0646\u0645\u0627\u0630\u062c OEM \u0627\u0644\u0645\u062e\u0635\u0635\u0629: 500 \u0642\u0637\u0639\u0629. \u0645\u0631\u0648\u0646\u0629 \u0641\u064a \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0623\u0648\u0644\u0649.',",
     "'faq-a1': 'MOQ 100 \u0642\u0637\u0639\u0629 \u0644\u0643\u0644 \u0637\u0631\u0627\u0632 \u0644\u0644\u0646\u0645\u0627\u0630\u062c \u0627\u0644\u0642\u064a\u0627\u0633\u064a\u0629 \u0648OEM. \u0645\u0631\u0648\u0646\u0629 \u0641\u064a \u0627\u0644\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0623\u0648\u0644\u0649.',"),
    ("'faq-a1': '\u6807\u51c6\u73b0\u8d27\u578b\u53f7\uff1a100\u4ef6\u8d77\u3002OEM\u5b9a\u5236\u578b\u53f7\uff1a500\u4ef6\u8d77\u3002\u9996\u6b21\u5408\u4f5c\u548c\u6837\u54c1\u8ba2\u5355\u53ef\u7075\u6d3b\u534f\u5546\u3002',",
     "'faq-a1': 'MOQ 100\u4ef6\uff0c\u73b0\u8d27\u4e0eOEM\u5b9a\u5236\u5747\u9002\u7528\u3002\u9996\u6b21\u5408\u4f5c\u548c\u6837\u54c1\u8ba2\u5355\u53ef\u7075\u6d3b\u534f\u5546\u3002',"),
]

# scan scope: html/txt/js, exclude 301 sources (*__*), tools, .git
import os
files = []
for root, dirs, fs in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '_tools']]
    for fn in fs:
        if not fn.endswith(('.html', '.txt', '.js')):
            continue
        if '__' in fn:
            continue
        files.append(os.path.join(root, fn))

data = {}
for p in files:
    data[p] = open(p, 'rb').read()

# Longest-first: a shorter rule's old-text may be a substring of a longer rule's
# old-text; applying short first would consume the longer target.
ordered = sorted(RULES, key=lambda x: -len(x[0]))

grand_old = 0
applied = 0
for o, n in ordered:
    ob, nb = o.encode('utf-8'), n.encode('utf-8')
    hits = []
    for p, b in data.items():
        c = b.count(ob)
        if c:
            hits.append((p, c))
    tot = sum(c for _, c in hits)
    grand_old += tot
    flag = ' *** NO HIT ***' if tot == 0 else ''
    print('hits=%-3d %s%s' % (tot, o[:58].replace('\n', ' '), flag))
    if not DRY:
        # A rule may legitimately hit 0 here if a longer rule already rewrote it.
        for p, c in hits:
            data[p] = data[p].replace(ob, nb)
            applied += c

if not DRY:
    for p, b in data.items():
        orig = open(p, 'rb').read()
        if b != orig:
            open(p, 'wb').write(b)

    # Post-write residual check: no BAER-owned MOQ "500" phrasing should remain.
    import re
    residual = []
    for p in files:
        b = open(p, 'rb').read().decode('utf-8', 'ignore')
        for m in re.finditer(r'.{0,50}(MOQ|Minimum order|\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649|\u8d77\u8ba2\u91cf|\u8ba2\u5355\u91cf).{0,60}500.{0,30}', b, re.I):
            seg = m.group(0)
            # keep industry-generic ranges and non-MOQ 500s (fpm/m3h/voltage)
            if '100-500' in seg or 'fpm' in seg or 'm3/h' in seg or 'm\u00b3/h' in seg:
                continue
            residual.append((p, re.sub(r'\s+', ' ', seg)))
    print('\n=== RESIDUAL BAER-MOQ 500 (should be 0) ===')
    for p, seg in residual:
        print('  ', p, '::', seg[:110])
    assert not residual, 'residual BAER MOQ 500 found: %d' % len(residual)

print('\nTOTAL rule hits(dry,original)=%d  applied=%d  mode=%s  files=%d'
      % (grand_old, applied, 'DRY' if DRY else 'APPLY', len(files)))
