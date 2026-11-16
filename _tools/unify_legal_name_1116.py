#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""公司英文法定名全站统一为无空格写法（2026-11-16 Olivia 确认：Co.,ltd 无空格）。

用法:
    python _tools/unify_legal_name_1116.py            # dry-run
    python _tools/unify_legal_name_1116.py --apply

规则:
- 字节级替换，完全不碰行尾（CRLF/LF 原样保留）
- 命中数与 dry-run 一致才落盘；落盘后复查残留变体必须为 0
- 只改英文法定名，不动 "Zhejiang Baer Appliance Technology"（旧名，About 页保留）
"""
import sys, os, re, glob

CANON = b"Zhejiang Baer Electrical Technology Co.,ltd"
# 允许的原有变体：大小写 Baer/BAER、逗号后有无空格、Ltd 后有无点
PAT = re.compile(rb"Zhejiang\s+(?:Baer|BAER)\s+Electrical\s+Technology\s+Co\.\s*,\s*Ltd\.?", re.I)
LEFTOVER = re.compile(rb"Zhejiang\s+(?:Baer|BAER)\s+Electrical\s+Technology\s+Co\.,(?!ltd)", re.I)


def main():
    apply = "--apply" in sys.argv
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files = [f for f in sorted(glob.glob("**/*.html", recursive=True))
             if "__" not in os.path.basename(f)]  # *__*.html 是 _redirects 的 301 源，不碰
    files += [f for f in ("llms.txt", "sitemap.xml") if os.path.exists(f)]
    total = 0
    changed = 0
    rows = []
    for f in files:
        raw = open(f, "rb").read()
        hits = PAT.findall(raw)
        if not hits:
            continue
        new, n = PAT.subn(CANON, raw)
        # 断言：替换次数 == 命中次数
        assert n == len(hits), (f, n, len(hits))
        total += n
        changed += 1
        rows.append((n, f))
        if apply:
            open(f, "wb").write(new)
    for n, f in sorted(rows, reverse=True):
        print(f"{n:>4}  {f}")
    print(f"--- {'APPLIED' if apply else 'DRY-RUN'}: {changed} files, {total} occurrences ---")
    if apply:
        bad = []
        for f in files:
            s = open(f, "rb").read()
            if LEFTOVER.search(s):
                bad.append(f)
        print("残留非统一写法:", bad if bad else "无")
        # 旧名（Appliance）不应被改动
        keep = sum(open(f, "rb").read().count(b"Appliance Technology") for f in files)
        print("旧名 Appliance Technology 保留处数:", keep)


if __name__ == "__main__":
    main()
