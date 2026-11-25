# -*- coding: utf-8 -*-
"""
首页 H1 后身份句改写（P0 AEO）。
- index.html: 静态 h-d2 文本（AI 爬虫/首访读这个）
- js/main.js: en / ar / zh 三语 h-d2 字典（回访 localStorage 会覆盖）
字节级替换，保持原 CRLF；先 dry-run 打印命中数，再落盘。
"""
import sys

SITE = "D:/WorkBuddy/2026-10-08-15-46-08/site"
DRY = "--dry-run" in sys.argv

OLD_EN = "Sleek designs with intelligent humidity sensors, delivering 26dB whisper-quiet performance for modern interiors."
NEW_EN = "Zhejiang Baer Electrical Technology Co.,ltd is an exhaust fan manufacturer in Shengzhou, China \u2014 CE / CB / CCC / ISO 9001, 1,000,000 units/year capacity, legal entity since 2017."

OLD_AR = "\u062a\u0635\u0645\u064a\u0645\u0627\u062a \u0623\u0646\u064a\u0642\u0629 \u0645\u0639 \u0645\u0633\u062a\u0634\u0639\u0631\u0627\u062a \u0627\u0644\u0631\u0637\u0648\u0628\u0629 \u0627\u0644\u0630\u0643\u064a\u0629\u060c \u0623\u062f\u0627\u0621 \u0647\u0627\u062f\u0626 26dB \u0644\u0644\u0645\u0633\u0627\u062d\u0627\u062a \u0627\u0644\u062f\u0627\u062e\u0644\u064a\u0629 \u0627\u0644\u062d\u062f\u064a\u062b\u0629."
NEW_AR = "\u0634\u0631\u0643\u0629 Zhejiang Baer Electrical Technology Co.,ltd \u0647\u064a \u0634\u0631\u0643\u0629 \u062a\u0635\u0646\u064a\u0639 \u0645\u0631\u0627\u0648\u062d \u0634\u0641\u0637 \u0641\u064a \u0634\u0646\u062a\u0634\u0648\u060c \u0627\u0644\u0635\u064a\u0646 \u2014 CE / CB / CCC / ISO 9001\u060c \u0628\u0637\u0627\u0642\u0629 \u0625\u0646\u062a\u0627\u062c\u064a\u0629 1,000,000 \u0648\u062d\u062f\u0629/\u0633\u0646\u0629\u060c \u062a\u0623\u0633\u0633\u062a \u0639\u0627\u0645 2017."

OLD_ZH = "\u667a\u80fd\u6e7f\u5ea6\u4f20\u611f\u5668\uff0c26dB\u8d85\u9759\u97f3\u8bbe\u8ba1\uff0c\u4e13\u4e3a\u73b0\u4ee3\u5ba4\u5185\u7a7a\u95f4\u6253\u9020\u3002"
NEW_ZH = "浙江巴尔电器科技有限公司（Zhejiang Baer Electrical Technology Co.,ltd）是位于中国嵊州的换气扇制造商 —— CE / CB / CCC / ISO 9001，年产能 100 万台，2017 年注册。"

print("NEW_EN len:", len(NEW_EN))
print("NEW_EN:", NEW_EN)


def patch(path, pairs, context_fmt):
    """pairs: list of (old_text, new_text); context_fmt: str.format(old)->full needle"""
    with open(path, "rb") as f:
        data = f.read()
    changed = False
    for old_t, new_t in pairs:
        needle = context_fmt.format(old_t).encode("utf-8")
        repl = context_fmt.format(new_t).encode("utf-8")
        n = data.count(needle)
        print("  {}: old_hits={}".format(path.split("/")[-1] + " :: " + old_t[:22], n))
        if n != 1:
            print("  !! SKIP (expected exactly 1 hit)")
            continue
        if not DRY:
            data = data.replace(needle, repl, 1)
            changed = True
    if not DRY and changed:
        with open(path, "wb") as f:
            f.write(data)
        print("  WRITTEN", path)
    return changed


print("\n== index.html (HTML static) ==")
patch(SITE + "/index.html",
      [(OLD_EN, NEW_EN)],
      '<p class="hero-desc" data-i18n="h-d2">{}</p>')

print("\n== js/main.js (en/ar/zh dictionary) ==")
patch(SITE + "/js/main.js",
      [(OLD_EN, NEW_EN,), (OLD_AR, NEW_AR), (OLD_ZH, NEW_ZH)],
      "'h-d2': '{}'")

print("\nDRY-RUN" if DRY else "\nAPPLIED")
