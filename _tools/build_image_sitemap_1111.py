#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add Google image-sitemap extensions to sitemap.xml.

Image sitemaps help Bing/Google discover images that JS-free crawls might
miss, and are the one actionable item left from the alt-text article
(Bing is BAER's only live traditional search channel).

Behaviour:
  * keeps every existing <url> block untouched (loc/lastmod/changefreq/priority)
  * inserts <image:image> nodes built from the page's own <img> tags
  * skips images whose file is missing on disk (no dead image URLs)
  * dedupes per page, caps at 20 images/page
  * idempotent: re-running rewrites the image blocks instead of duplicating
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
BASE = "https://baer-ventilation.com"
NS_IMAGE = "http://www.google.com/schemas/sitemap-image/1.1"
MAX_PER_PAGE = 20


def local_path_for(url):
    """Map a canonical URL back to the html file that renders it."""
    path = url[len(BASE):] if url.startswith(BASE) else url
    path = path.strip("/")
    if not path:
        return "index.html"
    for cand in (path + ".html", os.path.join(path, "index.html"), path):
        full = os.path.join(ROOT, cand.replace("/", os.sep))
        if os.path.isfile(full):
            return cand
    return None


def images_of(rel_file):
    """Extract (src, alt) pairs from a page, keeping only files that exist."""
    full = os.path.join(ROOT, rel_file.replace("/", os.sep))
    if not os.path.isfile(full):
        return []
    html = io.open(full, encoding="utf-8").read()
    out, seen = [], set()
    for m in re.finditer(r"<img\b([^>]*)>", html):
        attrs = m.group(1)
        src = re.search(r'\bsrc="([^"]+)"', attrs)
        if not src:
            continue
        src = src.group(1).strip()
        if src.startswith("data:") or src.startswith("http"):
            continue
        if not src.startswith("/"):
            src = "/" + src
        clean = src.split("?")[0]
        disk = os.path.join(ROOT, clean.lstrip("/").replace("/", os.sep))
        if not os.path.isfile(disk):
            continue
        if clean in seen:
            continue
        alt = re.search(r'\balt="([^"]*)"', attrs)
        title = re.sub(r"\s+", " ", (alt.group(1) if alt else "").strip())
        seen.add(clean)
        out.append((BASE + clean, title))
        if len(out) >= MAX_PER_PAGE:
            break
    return out


def main():
    raw = io.open(SITEMAP, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"

    # strip any previously generated image blocks (idempotent re-run)
    raw = re.sub(r"[ \t]*<image:image>.*?</image:image>\s*", "", raw, flags=re.S)

    # namespace declaration
    if "xmlns:image" not in raw:
        raw = raw.replace(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:image="%s">' % NS_IMAGE,
            1,
        )

    pages_with_images = 0
    total_images = 0

    def repl(m):
        nonlocal pages_with_images, total_images
        block = m.group(0)
        loc = re.search(r"<loc>([^<]+)</loc>", block)
        if not loc:
            return block
        rel = local_path_for(loc.group(1))
        if not rel:
            return block
        imgs = images_of(rel)
        if not imgs:
            return block
        pages_with_images += 1
        total_images += len(imgs)
        nodes = []
        for url, title in imgs:
            node = "    <image:image>" + nl + "      <image:loc>%s</image:loc>" % url
            if title:
                node += nl + "      <image:title>%s</image:title>" % (
                    title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                )
            node += nl + "    </image:image>"
            nodes.append(node)
        insert = "".join(n + nl for n in nodes)
        return block.replace("  </url>", insert + "  </url>", 1)

    new = re.sub(r"  <url>.*?</url>", repl, raw, flags=re.S)
    io.open(SITEMAP, "w", encoding="utf-8", newline="").write(new)
    print("pages with images: %d | image nodes: %d" % (pages_with_images, total_images))


if __name__ == "__main__":
    main()
