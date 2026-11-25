# -*- coding: utf-8 -*-
"""F01 RFQ unit + F02 Saudi example + homepage claim narrowing (Accio report 2026-11-25).
Byte-level, preserves CRLF. Dry-run prints hit counts. Idempotent (old_hits=0 on rerun).
"""
import sys

DRY = "--dry-run" in sys.argv

# (file, old, new)  -- all ASCII except ar/zh strings which are literal
R = [
    # ---- F01: RFQ unit error (divide by 60 -> m3/h is wrong) ----
    ("exhaust-fan-rfq-template.html",
     "Divide the result by 60 to convert from hours to minutes, and you have a target airflow in m3/h.",
     "In metric units that result is already an airflow in m3/h (cubic metres x ACH). If you measure the room in feet instead, multiply cubic feet by ACH and divide by 60 to get CFM."),

    # ---- F02: Saudi example duty point + electrical ----
    ("exhaust-fan-rfq-template.html",
     "<tr><td>Duty point</td><td>85 m3/h free air, 35 Pa static, below 42 dB(A) at 1 m</td></tr>",
     "<tr><td>Duty point</td><td>85 m3/h at 0 Pa (free air); airflow at 35 Pa static to be confirmed from the performance curve; below 42 dB(A) at 1 m</td></tr>"),
    ("exhaust-fan-rfq-template.html",
     "<tr><td>Electrical</td><td>220\u2013240 V / 50 Hz, ball-bearing motor, UK-style plug</td></tr>",
     "<tr><td>Electrical</td><td>220 V / 60 Hz (Saudi Arabia), ball-bearing motor; plug type to be confirmed with the customer</td></tr>"),

    # ---- homepage why-1d: remove 15-30% price claim (static + 3-lang) ----
    ("index.html",
     "Own factory in Zhejiang \u2014 no middlemen. Direct pricing is 15\u201330% lower than trading companies.",
     "Own factory in Zhejiang \u2014 no middlemen. Factory-direct pricing, quoted per order."),
    ("js/main.js",
     "50,000m\u00b2 own factory in Zhejiang. No middlemen \u2014 direct pricing means 15\u201330% lower cost vs trading companies.",
     "50,000m\u00b2 own factory in Zhejiang. No middlemen \u2014 factory-direct pricing, quoted per order."),
    ("js/main.js",
     "\u0645\u0635\u0646\u0639 \u062e\u0627\u0635 50,000\u0645\u00b2 \u0641\u064a \u0632\u064a\u062c\u064a\u0627\u0646\u063a. \u0628\u062f\u0648\u0646 \u0648\u0633\u0637\u0627\u0621 \u2014 \u0623\u0633\u0639\u0627\u0631 \u0623\u0642\u0644 \u0628\u0646\u0633\u0628\u0629 15\u201330% \u0645\u0642\u0627\u0631\u0646\u0629 \u0628\u0634\u0631\u0643\u0627\u062a \u0627\u0644\u062a\u062c\u0627\u0631\u0629.",
     "\u0645\u0635\u0646\u0639 \u062e\u0627\u0635 50,000\u0645\u00b2 \u0641\u064a \u0632\u064a\u062c\u064a\u0627\u0646\u063a. \u0628\u062f\u0648\u0646 \u0648\u0633\u0637\u0627\u0621 \u2014 \u062a\u0633\u0639\u064a\u0631 \u0645\u0628\u0627\u0634\u0631 \u0645\u0646 \u0627\u0644\u0645\u0635\u0646\u0639\u060c \u0645\u0639 \u0639\u0631\u0636 \u0633\u0639\u0631 \u062d\u0633\u0628 \u0627\u0644\u0637\u0644\u0628."),
    ("js/main.js",
     "\u6d59\u6c5f\u81ea\u6709\u5de5\u538250,000m\u00b2\uff0c\u65e0\u4e2d\u95f4\u5546\uff0c\u6bd4\u8d38\u6613\u516c\u53f8\u4ef7\u683c\u4f4e15\u201330%\u3002",
     "\u6d59\u6c5f\u81ea\u6709\u5de5\u538250,000m\u00b2\uff0c\u65e0\u4e2d\u95f4\u5546\uff0c\u5de5\u5382\u76f4\u4f9b\uff0c\u6309\u8ba2\u5355\u62a5\u4ef7\u3002"),

    # ---- homepage cert-desc: narrow blanket claim (static + 3-lang) ----
    ("index.html",
     "Every BAER product is tested and certified to meet global safety and performance standards.",
     "Certifications cover specific models and voltages; test reports are provided per order."),
    ("js/main.js",
     "Every BAER product is tested and certified to meet global safety and performance standards.",
     "Certifications cover specific models and voltages; test reports are provided per order."),
    ("js/main.js",
     "\u0643\u0644 \u0645\u0646\u062a\u062c BAER \u064a\u062e\u0636\u0639 \u0644\u0644\u0627\u062e\u062a\u0628\u0627\u0631 \u0648\u0627\u0644\u0627\u0639\u062a\u0645\u0627\u062f \u0648\u0641\u0642 \u0623\u0639\u0644\u0649 \u0645\u0639\u0627\u064a\u064a\u0631 \u0627\u0644\u0633\u0644\u0627\u0645\u0629 \u0627\u0644\u0639\u0627\u0644\u0645\u064a\u0629.",
     "\u062a\u063a\u0637\u064a \u0627\u0644\u0634\u0647\u0627\u062f\u0627\u062a \u0637\u0631\u0627\u0632\u0627\u062a \u0648\u062c\u0647\u0648\u062f\u0627\u064b \u0645\u062d\u062f\u062f\u0629\u060c \u0648\u062a\u064f\u0642\u062f\u0651\u0645 \u062a\u0642\u0627\u0631\u064a\u0631 \u0627\u0644\u0627\u062e\u062a\u0628\u0627\u0631 \u0645\u0639 \u0643\u0644 \u0637\u0644\u0628."),
    ("js/main.js",
     "\u6bcf\u6b3e BAER \u4ea7\u54c1\u5747\u7ecf\u8fc7\u6d4b\u8bd5\u548c\u8ba4\u8bc1\uff0c\u7b26\u5408\u5168\u7403\u5b89\u5168\u4e0e\u6027\u80fd\u6807\u51c6\u3002",
     "\u8ba4\u8bc1\u8986\u76d6\u5177\u4f53\u578b\u53f7\u4e0e\u7535\u538b\uff0c\u6d4b\u8bd5\u62a5\u544a\u6309\u8ba2\u5355\u63d0\u4f9b\u3002"),
]

# group by file
from collections import defaultdict
byfile = defaultdict(list)
for f, o, n in R:
    byfile[f].append((o, n))

total_old = 0
total_new = 0
for f, pairs in byfile.items():
    b = open(f, "rb").read()
    orig = b
    for o, n in pairs:
        ob, nb = o.encode("utf-8"), n.encode("utf-8")
        oh, nh = b.count(ob), b.count(nb)
        total_old += oh
        total_new += nh
        print("%-40s old=%d new=%d  %s" % (f, oh, nh, o[:48]))
        if not DRY:
            assert oh == 1, "expected exactly 1 old hit in %s for %r, got %d" % (f, o[:40], oh)
            b = b.replace(ob, nb, 1)
    if not DRY and b != orig:
        open(f, "wb").write(b)
        print("  -> WROTE", f)

print("\nTOTAL old_hits=%d new_already=%d  mode=%s" % (total_old, total_new, "DRY" if DRY else "APPLY"))
