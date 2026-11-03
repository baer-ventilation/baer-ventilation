# -*- coding: utf-8 -*-
"""2026-11-03: industrial 页补 "industrial fan / manufacturer / m3-h" 措辞；噪音页与风量指南补入链"""
import io, sys

SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"

def patch(fn, pairs):
    p = SITE + fn
    raw = open(p, "rb").read().decode("utf-8")
    for old, new, label in pairs:
        n = raw.count(old)
        if n != 1:
            print(f"  !! {fn} [{label}] matches={n} -- SKIP")
            continue
        raw = raw.replace(old, new)
        print(f"  ok {fn} [{label}]")
    open(p, "wb").write(raw.encode("utf-8"))

# 1) 工业页：hero 行加 m3/h
patch("industrial-exhaust-fans.html", [
    ("from <strong>984 to 4,500 CFM</strong>, built for continuous duty",
     "from <strong>984 to 4,500 CFM (1,670&ndash;7,650 m&sup3;/h)</strong>, built for continuous duty",
     "hero-m3h"),
    # 2) 工业页：导语补 industrial fan / manufacturer 自然措辞
    ("Choosing one is not about brand &mdash; it is about matching airflow and mounting to the space.",
     "Choosing an industrial fan is not about brand &mdash; it is about matching airflow and mounting to the space, and this applies whether you are replacing one unit on an existing wall or specifying a whole building. As a ventilation fan manufacturer in Zhejiang we build all four families below on the same lines, so the comparison is like for like.",
     "intro-industrial-fan"),
])

# 3) 噪音页 / 风量页：CTA 文案里补工业页与尺寸指南入链
patch("exhaust-fan-noise-levels-guide.html", [
    ("<p>Send your application, quantity and destination &mdash; our export team replies within one working day.</p>",
     '<p>Send your application, quantity and destination &mdash; our export team replies within one working day. Sizing a warehouse floor or workshop? Start with <a href="/industrial-exhaust-fans" style="color:#C0392B;font-weight:600;text-decoration:underline;">industrial exhaust fans</a>, and check the dB figures against the <a href="/exhaust-fan-sizes-guide" style="color:#C0392B;font-weight:600;text-decoration:underline;">size guide</a>.</p>',
     "cta-links"),
])

patch("exhaust-fan-airflow-calculation-guide.html", [
    ("<p>Send room sizes and application &mdash; our engineers reply with the airflow calculation and recommended models within one working day.</p>",
     '<p>Send room sizes and application &mdash; our engineers reply with the airflow calculation and recommended models within one working day. Sizing a production hall? The <a href="/industrial-exhaust-fans" style="color:#C0392B;font-weight:600;text-decoration:underline;">industrial exhaust fan</a> page carries our air-change table for warehouses, welding bays and loading docks.</p>',
     "cta-links"),
])
print("done")
