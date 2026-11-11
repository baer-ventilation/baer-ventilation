#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-publish quality gate for baer-ventilation.com pages.

Five gates, run before every deploy:
  G1 keyword placement   - primary keyword in <title>, <h1> and first <p>
  G2 title/desc length   - title <= 65 chars, meta description 140-160 chars
  G3 structure           - exactly one <h1>, h2 ids unique, TOC anchors resolve
  G4 links               - internal hrefs resolve to a real file/route
  G5 red lines + tone    - no price/SAA/shipping-time claims, no AI-cliche phrasing

Usage:
    python _tools/pre_publish_check.py                 # check pages changed vs HEAD
    python _tools/pre_publish_check.py a.html b.html    # check named pages
    python _tools/pre_publish_check.py --all            # whole site (slow, noisy)

Exit code 1 if any FAIL, so it can gate a deploy script.
"""
import html as H
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# phrases that read as machine-written filler; silent killers of E-E-A-T
AI_CLICHES = [
    "in today's fast-paced world", "in the ever-evolving", "unlock the power",
    "unlock the full potential", "elevate your", "seamlessly integrate",
    "game-changer", "game changer", "delve into", "it is worth noting that",
    "navigate the complexities", "a testament to", "revolutionize",
    "cutting-edge solution", "one-stop shop", "look no further",
    "when it comes to choosing", "rest assured",
]

# fact red lines agreed with Olivia (2026-11)
RED_LINES = [
    (r"(?i)\b\d+\s*(?:-|to|–)\s*\d+\s*(?:days?|weeks?)\s*(?:by sea|transit|shipping|delivery time)",
     "shipping transit time stated"),
    (r"(?i)\bprice\s*(?:list|per unit|starts at)", "price list phrasing"),
]

# words that legitimately accompany an SAA mention
SAA_OK = ("renew", "expir", "arrang", "request", "lapse", "not currently", "does not", "no longer")

# a currency amount is only a product-price leak when it sits next to pricing language
PRICE_CONTEXT = ("price", "quoted", "quotation", "quote", "per unit", "per pc", "per piece",
                 "per set", "each", "moq", "unit price", "cost per")


def saa_claim_without_qualifier(t):
    """Only flag 'SAA certification' style CLAIMS, not enumerations like 'CB, SAA and ETL'."""
    out = []
    for m in re.finditer(r"(?i)SAA\s*(?:certification|certified|approval|approved|compliant)"
                         r"|(?:certified|approved)\s+(?:to|for|under)\s+SAA", t):
        window = t[max(0, m.start() - 160): m.end() + 160]
        low = window.lower()
        if any(w in low for w in SAA_OK):
            continue          # qualified elsewhere in the sentence — fine
        snippet = text_of(window)[:120]
        out.append(snippet)
        if len(out) >= 3:
            break
    return out


def price_without_context(t):
    """Currency amounts only flagged when pricing language is in the same sentence."""
    out = []
    for m in re.finditer(r"(?:USD|US\$|\$|RMB|CNY|¥)\s?\d[\d,]*(?:\.\d+)?", t):
        tail = t[m.end(): m.end() + 1]
        if tail in ("B", "M", "K", "b"):
            continue          # order-of-magnitude values (project size, market size)
        ctx = text_of(t[max(0, m.start() - 160): m.end() + 120]).lower()
        if not any(k in ctx for k in PRICE_CONTEXT):
            continue          # e.g. electricity tariff, SABER fee, export value
        out.append("%s … %s" % (m.group(0), ctx[:110]))
        if len(out) >= 3:
            break
    return out



def read(p):
    return io.open(p, encoding="utf-8").read()


def text_of(fragment):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def url_of(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def target_exists(href):
    """Resolve an internal href to a file on disk."""
    path = href.split("#")[0].split("?")[0]
    if not path.startswith("/"):
        return True  # external / relative oddities: skip
    if path.startswith("/_") or path.endswith((".pdf", ".xml", ".txt", ".webp", ".jpg", ".png")):
        p = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
        return os.path.isfile(p)
    rel = path.strip("/")
    if not rel:
        return os.path.isfile(os.path.join(ROOT, "index.html"))
    cands = [rel + ".html", os.path.join(rel, "index.html"), rel]
    if "?" in href or href.endswith("/") or href.count("/") >= 2:
        cands.append(os.path.join(rel, "index.html"))
    return any(os.path.isfile(os.path.join(ROOT, c.replace("/", os.sep))) for c in cands)


def check_page(rel):
    full = os.path.join(ROOT, rel.replace("/", os.sep))
    t = read(full)
    # noindex redirect stubs (e.g. products.html -> /products/) are exempt
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', t, re.I):
        return [("SKIP", "G3", "noindex redirect stub — exempt")], 0, 0
    rows = []  # (level, gate, message)

    def add(lvl, gate, msg):
        rows.append((lvl, gate, msg))

    # ---------- G2 titles
    tm = re.search(r"<title>(.*?)</title>", t, re.S)
    title = H.unescape(text_of(tm.group(1))) if tm else ""
    if not title:
        add("FAIL", "G2", "no <title>")
    elif len(title) > 65:
        add("WARN", "G2", "title %d chars (>65): %s" % (len(title), title[:70]))
    dm = re.search(r'name="description"\s+content="([^"]*)"', t)
    desc = H.unescape(dm.group(1)) if dm else ""
    if not desc:
        add("FAIL", "G2", "no meta description")
    elif not (130 <= len(desc) <= 165):
        add("WARN", "G2", "description %d chars (target 140-160)" % len(desc))

    # ---------- G3 structure
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", t, re.S)
    if len(h1s) != 1:
        add("FAIL", "G3", "%d <h1> tags (must be exactly 1)" % len(h1s))
    ids = re.findall(r'<h2[^>]*id="([^"]+)"', t)
    dup = sorted({x for x in ids if ids.count(x) > 1})
    if dup:
        add("FAIL", "G3", "duplicate h2 ids: %s" % dup)
    broken = sorted({a for a in re.findall(r'href="#([a-z0-9\-]+)"', t) if a not in ids})
    if broken:
        add("WARN", "G3", "in-page anchors with no target: %s" % broken)
    h1_text = text_of(h1s[0]) if h1s else ""

    # ---------- G1 keyword placement (title/h1/first paragraph share a 2+-word phrase)
    first_p = re.search(r"<p[^>]*>(.*?)</p>", t, re.S)
    lead = text_of(first_p.group(1)) if first_p else ""
    words = lambda s: re.findall(r"[a-z]{4,}", s.lower())
    banned = {"with", "from", "that", "this", "your", "their", "when", "what", "have", "they", "will"}
    tset = set(words(title)) - banned
    hset = set(words(h1_text)) - banned
    lset = set(words(lead)) - banned
    shared = (tset & hset) or (tset & lset)
    if not shared:
        add("WARN", "G1", "title/h1/lead share no 4+ char keyword")

    # ---------- G4 links
    bad = []
    for href in set(re.findall(r'href="(/[^"]*)"', t)):
        if href.startswith("/#") or href.startswith("//"):
            continue
        if not target_exists(href):
            bad.append(href)
    if bad:
        add("FAIL", "G4", "dead internal links: %s" % bad[:6])

    # ---------- G5 red lines
    for pat, msg in RED_LINES:
        for m in re.finditer(pat, t):
            ctx = text_of(t[max(0, m.start() - 60): m.end() + 60])[:120]
            add("FAIL", "G5", "%s → …%s…" % (msg, ctx))
            break
    for snip in saa_claim_without_qualifier(t):
        add("FAIL", "G5", "SAA claim without renewal/expiry qualifier → …%s…" % snip)
    for snip in price_without_context(t):
        add("FAIL", "G5", "product price disclosed → %s" % snip)

    # ---------- G5 AI tone
    low = t.lower()
    hits = [c for c in AI_CLICHES if c in low]
    if hits:
        add("WARN", "G5", "AI-cliche phrasing: %s" % hits)

    # ---------- JSON-LD
    for i, m in enumerate(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S), 1):
        import json as _json
        try:
            _json.loads(m.group(1))
        except Exception as e:
            add("FAIL", "G3", "JSON-LD #%d invalid: %s" % (i, str(e)[:60]))

    return rows, len(title), len(desc)


def main():
    args = [a for a in sys.argv[1:] if a != "--all"]
    if "--all" in sys.argv:
        pages = [f for f in os.listdir(ROOT) if f.endswith(".html") and "__" not in f]
    elif args:
        pages = args
    else:
        out = subprocess.run(["git", "diff", "--name-only", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True).stdout.split()
        pages = [f for f in out if f.endswith(".html") and "__" not in f]
    if not pages:
        print("no html pages to check (pass filenames or --all)")
        return 0

    fails = 0
    for p in pages:
        rows, tl, dl = check_page(p)
        head = "%-46s title=%d desc=%d" % (p, tl, dl)
        if not rows:
            print("%s  PASS" % head)
            continue
        print("%s  %d issue(s)" % (head, len(rows)))
        for lvl, gate, msg in rows:
            if lvl == "FAIL":
                fails += 1
            print("   [%s] %s %s" % (lvl, gate, msg))
    print("\n%d page(s) checked, %d FAIL" % (len(pages), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
