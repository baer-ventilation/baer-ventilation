# -*- coding: utf-8 -*-
"""2026-11-09 修正图片插入位置:移除旧 figure,插到 section-tag/首个 h2 之前."""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p):
    with io.open(os.path.join(ROOT, p), "rb") as f:
        return f.read().decode("utf-8")

def wr(p, s):
    with io.open(os.path.join(ROOT, p), "wb") as f:
        f.write(s.encode("utf-8"))

PAGES = ["exhaust-fan-sizes-guide.html", "exhaust-fan-airflow-calculation-guide.html",
         "exhaust-fan-noise-levels-guide.html", "exhaust-fan-maintenance-guide.html",
         "exhaust-fan-certifications-guide.html", "saber-saso-exhaust-fan-certification.html",
         "commercial-kitchen-exhaust-fans.html", "exhaust-fan-shutter-types.html",
         "industrial-exhaust-fans.html"]

FIG_RE = re.compile(r'[ \t]*<figure style="margin:26px 0[^"]*">.*?</figure>\r?\n(\r?\n)?', re.S)

for page in PAGES:
    t = rd(page)
    # 1) 移除已插入的图片 figure
    t2, n = FIG_RE.subn("", t)
    assert n == 1, f"{page}: expected 1 figure, found {n}"
    # 2) 找首个 h2,回退到紧邻的 section-tag 之前
    h2 = t2.find("<h2")
    assert h2 > 0
    tag = '<span class="section-tag"'
    tp = t2.rfind(tag, 0, h2)
    if tp > 0 and "<h2" not in t2[tp:h2]:
        h2 = tp
    m = re.search(r'src="/images/([^"]+)" alt="([^"]*)" width="(\d+)" height="(\d+)"', "")
    img = re.search(r'src="(/images/[^"]+)" alt="([^"]*)" width="(\d+)" height="(\d+)"', t)  # 从旧文本取参数
    # 旧文本已被 subn 移除,改从 n=0 前的原文本提取——重新读一次原文件拿参数
    orig = rd(page)
    om = re.search(r'<img src="(/images/[^"]+)" alt="([^"]*)" width="(\d+)" height="(\d+)"', orig)
    assert om, f"{page}: no img in original"
    src, alt, w, h = om.group(1), om.group(2), om.group(3), om.group(4)
    capm = re.search(r'<figcaption[^>]*>([^<]*)</figcaption>', orig)
    cap = capm.group(1) if capm else ""
    EOL = "\r\n" if "\r\n" in t2 else "\n"
    fig = (
        '  <figure style="margin:26px 0;text-align:center;">' + EOL +
        f'    <img src="{src}" alt="{alt}" width="{w}" height="{h}" '
        'loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">' + EOL +
        f'    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">{cap}</figcaption>' + EOL +
        '  </figure>' + EOL + EOL
    )
    t2 = t2[:h2] + fig + t2[h2:]
    wr(page, t2)
    # 验证:figure 必须在 section-tag(若存在)之前
    fi = t2.find('<figure')
    st = t2.find(tag)
    ok = (st == -1) or (fi < st)
    print(f"{page:46s} fig@{fi} tag@{st} {'OK' if ok else 'BAD'}")
print("FIX DONE")
