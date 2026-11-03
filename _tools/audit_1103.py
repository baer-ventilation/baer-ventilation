import os, re, json, io, sys
from collections import defaultdict

ROOT = r"D:/WorkBuddy/2026-10-08-15-46-08/site"
pages = {}   # slug -> dict
for f in sorted(os.listdir(ROOT)):
    if not f.endswith(".html"):
        continue
    if "__" in f:   # redirect sources
        continue
    p = os.path.join(ROOT, f)
    raw = open(p, "r", encoding="utf-8", errors="ignore").read()
    slug = f[:-5]
    def g(pat):
        m = re.search(pat, raw, re.S | re.I)
        return m.group(1).strip() if m else ""
    pages[slug] = {
        "file": f,
        "title": g(r"<title>(.*?)</title>"),
        "desc": g(r'<meta\s+name="description"\s+content="([^"]*)"'),
        "canonical": g(r'rel="canonical"\s+href="([^"]*)"'),
        "h1": g(r"<h1[^>]*>(.*?)</h1>"),
        "robots": g(r'<meta\s+name="robots"\s+content="([^"]*)"'),
        "hreflang": len(re.findall(r'hreflang="', raw)),
        "jsonld": len(re.findall(r'application/ld\+json', raw)),
        "raw": raw,
    }

# internal links
inbound = defaultdict(set)
outbound = defaultdict(set)
for slug, d in pages.items():
    hrefs = re.findall(r'href="(/[^"#?]*)"', d["raw"])
    for h in hrefs:
        t = h.strip("/") or "index"
        t = t[:-5] if t.endswith(".html") else t
        if t in pages and t != slug:
            inbound[t].add(slug)
            outbound[slug].add(t)

sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
sm_urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
sm_slugs = set()
for u in sm_urls:
    s = u.rstrip("/").split("/")[-1]
    sm_slugs.add(s if s else "index")

print("pages(html, excl redirect src):", len(pages), "| sitemap:", len(sm_urls))
print("\n== A. 零入链（疑似孤儿页）==")
orphans = sorted([s for s in pages if not inbound[s] and s != "index"])
for s in orphans:
    print(f"  {s}  (words~{len(re.sub(r'<[^>]+>',' ',pages[s]['raw']).split())})")

print("\n== B. 入链最少的 8 页 ==")
for s in sorted([x for x in pages if x != "index"], key=lambda x: len(inbound[x]))[:8]:
    print(f"  {s}: in={len(inbound[s])} out={len(outbound[s])}")

print("\n== C. 三个新页入链明细 ==")
for s in ["industrial-exhaust-fans", "commercial-kitchen-exhaust-fans", "exhaust-fan-sizes-guide"]:
    if s in pages:
        print(f"  {s}: inbound={len(inbound[s])} -> {sorted(inbound[s])}")
        print(f"     outbound={len(outbound[s])}, hreflang={pages[s]['hreflang']}, jsonld={pages[s]['jsonld']}")

print("\n== D. title 长度异常 (>60) 或重复 ==")
tcount = defaultdict(list)
for s, d in pages.items():
    tcount[d["title"]].append(s)
for t, ss in tcount.items():
    if len(ss) > 1:
        print(f"  DUP: {ss} -> {t[:70]}")
for s, d in sorted(pages.items()):
    if len(d["title"]) > 60:
        print(f"  LONG {len(d['title'])}: {s} :: {d['title']}")

print("\n== E. description 缺失/过长(>160)/重复 ==")
dcount = defaultdict(list)
for s, d in pages.items():
    if not d["desc"]:
        print(f"  MISSING desc: {s}")
    elif len(d["desc"]) > 160:
        print(f"  LONG {len(d['desc'])}: {s}")
    dcount[d["desc"]].append(s)
for t, ss in dcount.items():
    if len(ss) > 1 and t:
        print(f"  DUP desc: {ss}")

print("\n== F. 无 JSON-LD / robots 异常 ==")
for s, d in sorted(pages.items()):
    if d["jsonld"] == 0:
        print(f"  no JSON-LD: {s}")
    if d["robots"] and "noindex" in d["robots"].lower():
        print(f"  NOINDEX: {s}")

print("\n== G. sitemap 与文件不一致 ==")
print("  in sitemap not file:", sorted(sm_slugs - set(pages))[:10])
print("  file not in sitemap:", sorted(set(pages) - sm_slugs)[:10])

# llms.txt
llms_path = os.path.join(ROOT, "llms.txt")
if os.path.exists(llms_path):
    llms = open(llms_path, encoding="utf-8").read()
    print("\n== H. llms.txt 覆盖 ==")
    for s in ["industrial-exhaust-fans", "commercial-kitchen-exhaust-fans", "exhaust-fan-sizes-guide"]:
        print(f"  {s}: {'YES' if s in llms else 'MISSING'}")
