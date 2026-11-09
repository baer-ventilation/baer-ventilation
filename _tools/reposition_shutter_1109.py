# -*- coding: utf-8 -*-
"""2026-11-09 shutter 页重定位:补 intake/through-ventilation 内容 + 锚文本改 ventilation shutters."""
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def rd(p):
    with io.open(os.path.join(ROOT, p), "rb") as f:
        return f.read().decode("utf-8")

def wr(p, s):
    with io.open(os.path.join(ROOT, p), "wb") as f:
        f.write(s.encode("utf-8"))

CRLF = "\r\n"

# ---------- 1) shutter 页本体 ----------
P = "exhaust-fan-shutter-types.html"
t = rd(P)
orig = t

# 1a. 导语补 through-wall 引言
old_intro = ("This guide covers the four ways the problem is solved and which one suits which climate.</p>")
new_intro = ("This guide covers the four ways the problem is solved and which one suits which climate "
             "&mdash; and because through-wall ventilation always has two openings, one for exhaust and one "
             "for fresh-air intake, there is a separate section below on through-wall ventilation shutters "
             "on the intake side.</p>")
assert t.count(old_intro) == 1, "intro not found"
t = t.replace(old_intro, new_intro)

# 1b. Type 4 之后、Comparison 之前插入新节
marker = "  <h2>Comparison</h2>"
section = (
    "  <h2>Through-Wall Ventilation Shutters: the Intake Side</h2>" + CRLF +
    "  <p>Most buyers treat a ventilation shutter as an exhaust accessory, but a through-ventilation "
    "scheme has two wall openings, and the intake one needs its own shutter. Air enters low on one side "
    "and leaves high on the other; whatever the exhaust fan pulls out must be replaced through the intake "
    "opening. Left open, that intake hole admits the same dust, sand, insects and wind-driven rain as an "
    "unshuttered exhaust.</p>" + CRLF +
    "  <ul>" + CRLF +
    "    <li><strong>Gravity blades, reversed logic.</strong> An intake shutter works like an auto-shutter "
    "but is driven by the pressure difference the exhaust fan creates: while the fan runs it pulls the "
    "intake blades open, and they fall closed when it stops. No power, no controls.</li>" + CRLF +
    "    <li><strong>Free area first.</strong> The intake shutter must not strangle the fan. Match its free "
    "area to at least the fan's, and a common rule is to size the intake opening 20&ndash;30% larger than "
    "the exhaust opening so static pressure stays low. The free-area arithmetic is the same one used in the "
    "commercial submittal section above.</li>" + CRLF +
    "    <li><strong>Insect and bird mesh.</strong> On the intake side mesh matters more than on exhaust, "
    "because incoming air carries seeds and insects into the workspace. A stainless bird screen outside "
    "plus a fine insect mesh inside is standard in Gulf installations.</li>" + CRLF +
    "    <li><strong>Sand and rain orientation.</strong> On desert and coastal facades, pair the intake "
    "shutter with an external weather louvre and keep the intake away from the prevailing wind &mdash; the "
    "<a href=\"/exhaust-fan-middle-east-climate\">Middle East climate guide</a> covers the siting detail.</li>" + CRLF +
    "    <li><strong>Kitchens and make-up air.</strong> A commercial extract canopy without a matched "
    "intake starves the fan and drags air down the grease duct. The intake shutter is what lets make-up "
    "air in on demand &mdash; see the <a href=\"/commercial-kitchen-exhaust-fans\">commercial kitchen "
    "exhaust guide</a>.</li>" + CRLF +
    "  </ul>" + CRLF +
    "  <p>Specified as a pair &mdash; a gravity auto-shutter on the exhaust fan and a gravity intake "
    "shutter with mesh on the opposite wall &mdash; a through-wall ventilation set costs little more than "
    "the fan alone and closes both holes when the system stops.</p>" + CRLF + CRLF
)
assert t.count(marker) == 1, "comparison marker not found"
t = t.replace(marker, section + marker)

# 1c. FAQ 末尾加一条
faq_anchor = "  <h3>Can I add a shutter to a fan that does not have one?</h3>"
faq_new = (
    "  <h3>What is a through ventilation shutter?</h3>" + CRLF +
    "  <p>It is the shutter fitted on the intake opening of a through-wall ventilation scheme &mdash; the "
    "hole that replaces the air the exhaust fan removes. It works on the same gravity principle as the "
    "exhaust auto-shutter: it opens while the fan runs and falls closed when the fan stops. Because the "
    "intake brings outside air in, it always carries an insect mesh and, in dusty or coastal regions, an "
    "external weather louvre as well.</p>" + CRLF + CRLF
)
assert t.count(faq_anchor) == 1, "faq anchor not found"
t = t.replace(faq_anchor, faq_new + faq_anchor)

# 1d. 更新日期
t = t.replace("Last updated: October 20, 2026", "Last updated: November 9, 2026")

assert t != orig
wr(P, t)
print("shutter page patched, bytes:", len(t))

# ---------- 2) 锚文本改 ventilation shutters 变体 ----------
ANCHORS = [
    ("exhaust-fans.html",
     ">Exhaust shutters and fan shutter types explained</a>",
     ">Ventilation shutters: types explained (exhaust and intake)</a>"),
    ("cfm-calculator.html",
     ">exhaust shutter types guide</a>",
     ">ventilation shutters and shutter types</a>"),
    ("exhaust-fan-middle-east-climate.html",
     ">Exhaust Fan Shutter Types Explained</a>",
     ">Ventilation Shutters for Middle East Installations</a>"),
    ("exhaust-fan-airflow-calculation-guide.html",
     ">Exhaust Fan Shutter Types</a>",
     ">Ventilation Shutter Types</a>"),
    ("inline-duct-fan-vs-axial-fan.html",
     ">Exhaust Fan Shutter Types Explained</a>",
     ">Ventilation Shutters Explained</a>"),
    ("panel-exhaust-fan-installation-guide.html",
     ">Exhaust Fan Shutter Types Explained</a>",
     ">Ventilation Shutter Types Guide</a>"),
    ("products/index.html",
     ">exhaust shutters and fan shutter types</a>",
     ">ventilation shutter types</a>"),
    ("klt-series-panel-exhaust-fan.html",
     ">What are exhaust shutters? Types explained</a>",
     ">What are ventilation shutters? Types explained</a>"),
]
for path, old, new in ANCHORS:
    s = rd(path)
    assert s.count(old) == 1, f"{path}: anchor not unique/found ({old!r})"
    wr(path, s.replace(old, new))
    print("anchor ok:", path)

print("ALL DONE")
