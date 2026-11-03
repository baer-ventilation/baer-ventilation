import os, re
from collections import defaultdict

ROOT = r"D:/WorkBuddy/2026-10-08-15-46-08/site"
pages = {}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in ("_tools", "assets", "css", "js", ".git")]
    for f in filenames:
        if not f.endswith(".html") or "__" in f:
            continue
        full = os.path.join(dirpath, f)
        rel = os.path.relpath(full, ROOT).replace("\\", "/")
        slug = rel[:-5]
        if slug.endswith("/index"):
            slug = slug[: -len("index")].rstrip("/")
        elif slug == "index":
            slug = ""
        raw = open(full, encoding="utf-8", errors="ignore").read()
        pages[slug] = {"rel": rel, "raw": raw}

inbound = defaultdict(set)
outbound = defaultdict(set)
for slug, d in pages.items():
    for h in re.findall(r'href="(/[^"#?]*)"', d["raw"]):
        t = h.strip("/")
        t = re.sub(r"\.html$", "", t)
        if t.endswith("/index"):
            t = t[: -len("index")].rstrip("/")
        if t in pages and t != slug:
            inbound[t].add(slug)
            outbound[slug].add(t)

content = [s for s in pages if s and not s.startswith(("zh", "ar"))]
print("total html:", len(pages), "| en content pages:", len(content))
print("\n== 入链 0-2 的英文内容页 ==")
for s in sorted(content, key=lambda x: len(inbound[x])):
    if len(inbound[s]) <= 2:
        print(f"  in={len(inbound[s])} out={len(outbound[s])}  {s or '(home)'}")

print("\n== 三新页（含目录页统计）==")
for s in ["industrial-exhaust-fans", "commercial-kitchen-exhaust-fans", "exhaust-fan-sizes-guide"]:
    print(f"  {s}: in={len(inbound[s])} {sorted(inbound[s])}")

print("\n== hreflang 明细（三新页）==")
for s in ["industrial-exhaust-fans", "commercial-kitchen-exhaust-fans", "exhaust-fan-sizes-guide"]:
    for m in re.finditer(r'<link[^>]+hreflang="([^"]+)"[^>]*>', pages[s]["raw"]):
        print(f"  {s}: {m.group(0)[:150]}")
