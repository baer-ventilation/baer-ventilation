#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the 10th photo to the SABER guide. Byte-level, CRLF-safe, idempotent."""
import sys
PATH = "saber-saso-exhaust-fan-certification.html"
APPLY = "--apply" in sys.argv
with open(PATH, "rb") as f:
    raw = f.read()
assert raw.count(b"\r\n") > 400 and raw.count(b"\n") == raw.count(b"\r\n")
NL = "\r\n"
text = raw.decode("utf-8")
marker = "<!-- EXPANDED:saber-fig10-showroom -->"
if marker in text:
    print("SKIP already applied")
    sys.exit(0)
anchor = '<h2>What BAER Supplies</h2>'
assert text.count(anchor) == 1, text.count(anchor)
block = (
    marker + NL +
    '<figure style="margin:26px 0;text-align:center;">' + NL +
    '  <img src="/images/showroom-wall" alt="BAER showroom displaying exhaust fan product ranges" width="960" height="640" loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">' + NL +
    '  <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Product ranges on display — model-by-model specification sheets help an importer register each variant accurately the first time.</figcaption>' + NL +
    '</figure>' + NL + anchor
)
print("DRY RUN: would insert showroom photo before", anchor)
if not APPLY:
    sys.exit(0)
text = text.replace(anchor, block, 1)
out = text.encode("utf-8")
assert out.count(b"\n") == out.count(b"\r\n"), "CRLF broken"
with open(PATH, "wb") as f:
    f.write(out)
print("WRITTEN bytes", len(out))
