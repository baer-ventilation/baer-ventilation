#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix missing .webp extension on 9 image src paths in SABER guide."""
import sys
PATH = "saber-saso-exhaust-fan-certification.html"
APPLY = "--apply" in sys.argv
with open(PATH, "rb") as f:
    raw = f.read()
assert raw.count(b"\n") == raw.count(b"\r\n")
text = raw.decode("utf-8")
names = [
    "baer-certificate-wall", "baer-export-cartons-warehouse",
    "baer-factory-sign-legal-name", "baer-hi-pot-test", "baer-sample-room",
    "motor-test-bench", "panel-fan-assembly-line", "showroom-wall", "winding-station",
]
total = 0
for n in names:
    old = 'src="/images/%s"' % n
    new = 'src="/images/%s.webp"' % n
    c = text.count(old)
    if c == 0 and new in text:
        print("SKIP already fixed:", n)
        continue
    if c != 1:
        print("FAIL count", c, n); sys.exit(1)
    if APPLY:
        text = text.replace(old, new, 1)
    total += 1
    print("FIX", n)
print("TOTAL", total)
if not APPLY:
    print("DRY RUN"); sys.exit(0)
out = text.encode("utf-8")
assert out.count(b"\n") == out.count(b"\r\n")
with open(PATH, "wb") as f:
    f.write(out)
print("WRITTEN", len(out))
