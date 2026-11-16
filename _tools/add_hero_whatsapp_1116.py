#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 WhatsApp 主 CTA 提到中东落地页首屏（hero 内、首段正文之前）。

用法:
    python _tools/add_hero_whatsapp_1116.py            # dry-run，只打印计划
    python _tools/add_hero_whatsapp_1116.py --apply    # 落盘

规则（2026-11-16 立）:
- 逐文件自适应行尾（saudi 等页为 LF，其余 CRLF），不整文件重写行尾
- 幂等：已存在 hero-cta 的文件直接跳过
- 每处插入都断言命中数，落盘后复核 wa.me 计数 +1
"""
import sys, os, io, re

PAGES = {
    "qatar-exhaust-fan-supplier.html": "Qatar",
    "oman-exhaust-fan-supplier.html": "Oman",
    "saudi-arabia-exhaust-fan-supplier.html": "Saudi%20Arabia",
    "middle-east-exhaust-fan-supplier.html": "the%20Middle%20East",
}

ANCHOR_RE = re.compile(r'[ \t]*<p style="font-size:13px;color:#[0-9A-Fa-f]{6};margin:10px 0 0;">Last updated:')
CSS_ANCHOR = ".btn-outline { display: inline-block;"

CSS_ADD = """.hero-cta { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin: 26px 0 0; }
.hero-cta a { margin: 0; }
.btn-wa { display: inline-block; background: #25D366; color: #fff !important; padding: 14px 32px; border-radius: 6px; font-weight: 700; text-decoration: none; font-size: 15px; }
.btn-wa:hover { background: #1fb857; }
.hero-trust { font-size: 13px; color: #CBD5E1; margin: 12px 0 0 !important; }"""

BLOCK = """  <div class="hero-cta">
    <a class="btn-wa" href="https://wa.me/8613655859122?text=Hello%20BAER%2C%20I%27m%20looking%20for%20exhaust%20fans%20for%20{country}.%20Please%20send%20catalog%20and%20price%20for%3A%20" target="_blank" rel="noopener">Chat on WhatsApp</a>
    <a class="btn-outline" href="mailto:sunny@zjbaer.com?subject=Exhaust%20fan%20enquiry%20-%20{country}">Email your spec sheet</a>
  </div>
  <p class="hero-trust">Reply within one working day &middot; send your model list or drawings for a factory-direct quote</p>"""


def line_start(s, idx):
    return s.rfind("\n", 0, idx) + 1


def process(path, country, apply=False):
    raw = open(path, "rb").read()
    nl = "\r\n" if raw.count(b"\r\n") > 0 else "\n"
    s = raw.decode("utf-8")
    # 统一成 LF 处理，最后整体按原行尾写回
    work = s.replace("\r\n", "\n")
    crlf_ratio_ok = (raw.count(b"\r\n") == 0) or (raw.count(b"\r\n") == raw.count(b"\n"))
    rep = {"file": path, "nl": "CRLF" if nl == "\r\n" else "LF", "crlf_ratio_ok": crlf_ratio_ok}
    if "hero-cta" in work:
        rep["action"] = "SKIP(已存在)"
        return rep, None

    # 1) CSS
    assert work.count(CSS_ANCHOR) == 1, f"{path}: CSS 锚点命中 {work.count(CSS_ANCHOR)}"
    i = work.find(CSS_ANCHOR)
    j = work.find("\n", i) + 1
    work = work[:j] + CSS_ADD.replace("\n", "\n") + "\n" + work[j:]

    # 2) hero CTA 区块
    hits = list(ANCHOR_RE.finditer(work))
    assert len(hits) == 1, f"{path}: 正文锚点命中 {len(hits)}"
    k = hits[0].start()
    work = work[:k] + BLOCK.format(country=country) + "\n" + work[k:]

    # 2b) 顺手修 saudi 页深色 hero 上 #64748B 的对比度问题（不可读）
    work = work.replace('color:#64748B;margin:10px 0 0;">Last updated:',
                        'color:#CBD5E1;margin:10px 0 0;">Last updated:')

    # 3) 复核
    assert work.count("hero-cta") == 3, f"{path}: hero-cta 计数 {work.count('hero-cta')}"  # css 1 + div class 1 + 规则里 1
    assert work.count("wa.me") == 2, f"{path}: wa.me 计数 {work.count('wa.me')}"
    assert work.count("btn-wa") == 3, f"{path}: btn-wa 计数 {work.count('btn-wa')}"

    out = work.replace("\n", nl) if nl == "\r\n" else work
    rep["added_bytes"] = len(out.encode("utf-8")) - len(raw)
    rep["action"] = "WRITE" if apply else "DRY-RUN OK"
    return rep, (out.encode("utf-8") if apply else None)


def main():
    apply = "--apply" in sys.argv
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for f, c in PAGES.items():
        rep, data = process(f, c, apply)
        print(f"{rep['action']:12s} {f:42s} nl={rep['nl']:4s} crlf_ok={rep['crlf_ratio_ok']} "
              f"added={rep.get('added_bytes', '-')}")
        if data:
            open(f, "wb").write(data)
    print("APPLIED" if apply else "DRY-RUN ONLY (加 --apply 落盘)")


if __name__ == "__main__":
    main()
