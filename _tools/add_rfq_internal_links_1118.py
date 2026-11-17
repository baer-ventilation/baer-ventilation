#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 /exhaust-fan-rfq-template 从 6 个枢纽/决策页链出去，消除孤儿页。
逐文件自适应行尾；幂等（已有 rfq 链接则跳过）；dry-run 默认，--apply 落盘。
不碰标题/meta/正文，只在既有链接区块追加一条链接。
"""
import sys

APPLY = "--apply" in sys.argv

# file -> (唯一锚点, 要追加的链接行[str], 说明)
PLAN = {
    "resources.html": (
        '<a href="/exhaust-fan-moq-guide">Read the MOQ &amp; pricing guide \u2192</a></article>',
        '<article class="card"><span class="tag">Procurement</span><h2>Exhaust Fan RFQ Template</h2>'
        '<p>A ready-to-copy 20-item enquiry template - airflow, voltage, motor, mounting and certification - '
        'so you get an accurate factory quotation in one round.</p>'
        '<a href="/exhaust-fan-rfq-template">Download the RFQ template \u2192</a></article>',
        "资源页 Procurement 卡片",
    ),
    "exhaust-fans.html": (
        '<li><a href="/cfm-calculator" style="color:#C0392B;font-weight:700;text-decoration:none;">CFM Calculator</a></li>',
        '<li><a href="/exhaust-fan-rfq-template" style="color:#C0392B;font-weight:700;text-decoration:none;">'
        'Exhaust Fan RFQ Template (20 items to specify)</a></li>',
        "品类枢纽 Related Guides",
    ),
    "exhaust-fan-moq-guide.html": (
        '<li><a href="/exhaust-fan-container-loading-guide" style="color:#C0392B;font-weight:700;text-decoration:none;">Container Loading Guide (20GP / 40GP / 40HQ)</a></li>',
        '<li><a href="/exhaust-fan-rfq-template" style="color:#C0392B;font-weight:700;text-decoration:none;">'
        'Exhaust Fan RFQ Template (send your spec in one round)</a></li>',
        "MOQ 指南 相关链接",
    ),
    "exhaust-fan-certifications-guide.html": (
        '<li><a href="/panel-exhaust-fan-oem-spec-sheet">Panel Exhaust Fan OEM Spec Sheet</a></li>',
        '<li><a href="/exhaust-fan-rfq-template">Exhaust Fan RFQ Template (specify certification needs)</a></li>',
        "认证指南 Related Articles",
    ),
    "index.html": (
        '<a class="baer-btn-v2" href="/oem-private-label-exhaust-fan-guide">OEM & Private Label</a>',
        '<a class="baer-btn-v2" href="/exhaust-fan-rfq-template">RFQ Template</a>',
        "首页 CTA 按钮组",
    ),
    "products/index.html": (
        '<li><a href="/exhaust-fan-airflow-calculation-guide">Airflow calculation guide</a></li>',
        '<li><a href="/exhaust-fan-rfq-template">RFQ template \u2014 send all 20 specs in one round</a></li>',
        "产品页 选型步骤链接",
    ),
}

changed = 0
for path, (anchor, line, desc) in PLAN.items():
    raw = open(path, "rb").read()
    s = raw.decode("utf-8")
    if "/exhaust-fan-rfq-template" in s:
        print(f"SKIP  {path} ({desc}) - already linked")
        continue
    assert s.count(anchor) == 1, f"{path}: anchor count={s.count(anchor)}"
    i = s.find(anchor) + len(anchor)
    # 自适应行尾：看锚点后紧跟的是 \r\n 还是 \n
    nl = "\r\n" if s[i:i+2] == "\r\n" else ("\n" if s[i:i+1] == "\n" else "\r\n")
    new = s[:i] + nl + line + s[i:]
    tag = "APPLY" if APPLY else "DRY  "
    print(f"{tag}  {path:42s} nl={'CRLF' if nl==chr(13)+chr(10) else 'LF'}  +{len(line)}ch  {desc}")
    if APPLY:
        open(path, "wb").write(new.encode("utf-8"))
        changed += 1

print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {changed} files changed")
