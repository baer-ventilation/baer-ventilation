# -*- coding: utf-8 -*-
"""修复两类问题：1) 10页认证措辞 2) 风量指南ACH口径冲突。字节级替换，保护CRLF。先 dry-run。"""
import os, sys, json, re

DRY = "--apply" not in sys.argv
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

AUTH_OLD = "CE, CB and ISO 9001 certified since 2003"
AUTH_NEW = "CE, CB and ISO 9001 certified; factory heritage since 2003"

# ACH: 正文表格行
ACH_ROW_OLD = "<tr><td>Commercial kitchen hood exhaust</td><td>30\u201360 (by hood design)</td></tr>"
ACH_ROW_NEW = "<tr><td>Commercial kitchen cooking hood (local exhaust)</td><td>30\u201360 (hood-capture sizing by design; not a room ACH \u2014 see FAQ)</td></tr>"

# ACH: FAQ 句子（可见版 + JSON-LD 各一次，共享同一子串）
ACH_QA_OLD = ("Residential bathrooms need 8 ACH; commercial kitchens and humid Gulf-climate "
              "spaces need 10-15 ACH; warehouses and factories typically 6-10 ACH based on "
              "heat and pollutant load. Round up to the nearest standard fan size.")
ACH_QA_NEW = ("Residential bathrooms need 8 ACH; size commercial kitchen room ventilation at "
              "10-15 ACH and humid Gulf-climate rooms at 10-15 ACH; a cooking hood is a separate "
              "local-exhaust calculation (often 30-60 by hood design), not a room ACH value; "
              "warehouses and factories typically 6-10 ACH based on heat and pollutant load. "
              "Round up to the nearest standard fan size.")

AIRFLOW = "exhaust-fan-airflow-calculation-guide.html"

def readb(p): return open(p, "rb").read()
def writeb(p, b): open(p, "wb").write(b)

print("MODE:", "DRY-RUN (no write)" if DRY else "APPLY")
total = 0

# ---- 1. 认证措辞 10 页 ----
auth_files = []
for fn in sorted(os.listdir(".")):
    if not fn.endswith(".html"): continue
    b = readb(fn)
    n = b.count(AUTH_OLD.encode())
    if n: auth_files.append((fn, n))

print("\n[1] 认证措辞命中(旧):")
for fn, n in auth_files:
    print(f"   {fn}: {n}")
new_phrase_files = [(fn, readb(fn).decode().count(AUTH_NEW)) for fn in sorted(os.listdir("."))
                    if fn.endswith(".html") and AUTH_NEW in readb(fn).decode()]
new_total = sum(n for _, n in new_phrase_files)
# 幂等：已全部应用则直接退出
if not auth_files and new_total == 10:
    print(f"\nIDEMPOTENT: 旧措辞 0 处、新措辞 {new_total} 处 → 已应用过，0 变更，跳过")
    sys.exit(0)
assert len(auth_files) == 10, f"expected 10 files with old phrase, got {len(auth_files)} (new={new_total})"
assert all(n == 1 for _, n in auth_files), "sample file hit != 1"
sample = readb(auth_files[0][0]).decode()
i = sample.find(AUTH_OLD)
print("   SAMPLE:", repr(sample[i-60:i+len(AUTH_OLD)+40]))

# ---- 2. ACH 冲突 ----
b = readb(AIRFLOW).decode()
n_row = b.count(ACH_ROW_OLD)
n_qa = b.count(ACH_QA_OLD)
print("\n[2] ACH 命中:")
print(f"   {AIRFLOW} 表格行: {n_row} (expect 1)")
print(f"   {AIRFLOW} FAQ句: {n_qa} (expect 2 = 可见版+JSON-LD)")
print("   ROW SAMPLE:", repr(b[b.find(ACH_ROW_OLD):b.find(ACH_ROW_OLD)+len(ACH_ROW_OLD)]))
print("   QA SAMPLE:", repr(b[b.find(ACH_QA_OLD):b.find(ACH_QA_OLD)+70]))
assert n_row == 1 and n_qa == 2, "ACH hit count mismatch"

# 幂等检查
already = readb("exhaust-fans.html").decode().count(AUTH_NEW)
print("\n[3] 幂等检查: 新措辞已存在数 =", already, "(expect 0 on first run)")
if already == 10 and not DRY:
    print("   -> 已应用过，跳过写入")
    sys.exit(0)

# JSON-LD FAQ 数（改后要保持一致）
lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', b, re.S)
faq_count = 0
for ld in lds:
    try:
        o = json.loads(ld)
        if o.get("@type") == "FAQPage": faq_count = len(o.get("mainEntity", []))
    except Exception: pass
print("   FAQPage JSON-LD 问题数:", faq_count)

# ---- 落盘 ----
if not DRY:
    total = 0
    for fn, n in auth_files:
        raw = readb(fn)
        assert raw.count(AUTH_OLD.encode()) == 1
        raw2 = raw.replace(AUTH_OLD.encode(), AUTH_NEW.encode())
        assert raw2.count(b"\r\r\n") == 0, f"double CR in {fn}"
        writeb(fn, raw2); total += 1
    print(f"\nAPPLIED: 认证措辞 {total} 页")

    raw = readb(AIRFLOW).decode()
    raw2 = raw.replace(ACH_ROW_OLD, ACH_ROW_NEW).replace(ACH_QA_OLD, ACH_QA_NEW)
    assert raw2.count(ACH_ROW_NEW) == 1 and raw2.count(ACH_QA_NEW) == 2
    b2 = raw2.encode()
    assert b2.count(b"\r\r\n") == 0, "double CR in airflow"
    writeb(AIRFLOW, b2)
    print("APPLIED: ACH 表格1 + FAQ 2 处")

    # 改后校验
    for fn, _ in auth_files:
        s = readb(fn).decode()
        assert AUTH_OLD not in s and AUTH_NEW in s, f"verify fail {fn}"
    vf = readb(AIRFLOW).decode()
    assert ACH_ROW_OLD not in vf and ACH_QA_OLD not in vf
    # JSON-LD 仍可解析且 FAQ 数不变
    lds2 = re.findall(r'<script type="application/ld\+json">(.*?)</script>', vf, re.S)
    c2 = 0
    for ld in lds2:
        o = json.loads(ld)
        if o.get("@type") == "FAQPage": c2 = len(o.get("mainEntity", []))
    assert c2 == faq_count, f"FAQ count changed {faq_count}->{c2}"
    # 可见 FAQ 与 JSON-LD 文本一致
    assert ACH_QA_NEW in vf
    print("VERIFY: 10页措辞 + ACH 3处 + JSON-LD可解析 + FAQ数不变 + 无double CR 全过")
else:
    print("\nDRY-RUN OK — 未写入。加 --apply 执行。")
