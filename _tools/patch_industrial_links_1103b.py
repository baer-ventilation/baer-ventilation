# -*- coding: utf-8 -*-
"""2026-11-03: 噪音页 / 风量页 CTA 里补工业页与尺寸指南入链（用真 em dash）"""
SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"

def patch(fn, old, new, label):
    p = SITE + fn
    raw = open(p, "rb").read().decode("utf-8")
    n = raw.count(old)
    if n != 1:
        print(f"  !! {fn} [{label}] matches={n} -- SKIP")
        return
    open(p, "wb").write(raw.replace(old, new).encode("utf-8"))
    print(f"  ok {fn} [{label}]")

patch("exhaust-fan-noise-levels-guide.html",
      "<p>Send your application, quantity and destination \u2014 our export team replies within one working day.</p>",
      '<p>Send your application, quantity and destination \u2014 our export team replies within one working day. Sizing a warehouse floor or workshop? Start with <a href="/industrial-exhaust-fans" style="color:#C0392B;font-weight:600;text-decoration:underline;">industrial exhaust fans</a>, and check the dB figures against the <a href="/exhaust-fan-sizes-guide" style="color:#C0392B;font-weight:600;text-decoration:underline;">size guide</a>.</p>',
      "cta-links")

patch("exhaust-fan-airflow-calculation-guide.html",
      "<p>Send room sizes and application \u2014 our engineers reply with the airflow calculation and recommended models within one working day.</p>",
      '<p>Send room sizes and application \u2014 our engineers reply with the airflow calculation and recommended models within one working day. Sizing a production hall? The <a href="/industrial-exhaust-fans" style="color:#C0392B;font-weight:600;text-decoration:underline;">industrial exhaust fan</a> page carries our air-change table for warehouses, welding bays and loading docks.</p>',
      "cta-links")
print("done")
