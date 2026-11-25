#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shorten GB 29539 page meta description to target length across all tags."""
import sys
PATH = "gb-29539-2025-ventilating-fan-energy-efficiency.html"
APPLY = "--apply" in sys.argv
with open(PATH, "rb") as f:
    raw = f.read()
assert raw.count(b"\n") == raw.count(b"\r\n")
text = raw.decode("utf-8")
old = "GB 29539-2025 took effect 1 Nov 2026: 3 energy grades, standby/off-mode limits and DC fans in scope. What applies, what is excluded, and how export buyers should read it."
new = "GB 29539-2025 took effect 1 Nov 2026: 3 energy grades, standby limits and DC fans in scope. What applies, what is excluded, and how export buyers read it."
print("old len", len(old), "new len", len(new))
c = text.count(old)
print("occurrences", c)
assert c == 4, c  # meta, og, twitter, jsonld
if not APPLY:
    print("DRY RUN"); sys.exit(0)
text = text.replace(old, new)
out = text.encode("utf-8")
assert out.count(b"\n") == out.count(b"\r\n")
with open(PATH, "wb") as f:
    f.write(out)
print("WRITTEN", len(out))
