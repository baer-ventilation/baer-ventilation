# -*- coding: utf-8 -*-
"""Fix missing .spec-table / .twrap / .tnote CSS on the two new pages (they shipped unstyled)."""
SITE = r"D:/WorkBuddy/2026-10-08-15-46-08/site/"

TBL_CSS = """/* spec tables */
.twrap{overflow-x:auto;margin:0 0 6px;}
.spec-table{width:100%;border-collapse:collapse;font-size:13.5px;background:#fff;}
.spec-table th{background:var(--dark);color:#fff;padding:11px 14px;text-align:left;font-weight:700;font-size:13px;}
.spec-table td{padding:11px 14px;border-bottom:1px solid var(--line);color:var(--text);vertical-align:top;}
.spec-table tr:nth-child(even) td{background:var(--light);}
.spec-table a{color:#C0392B;font-weight:700;}
.tnote{font-size:12.5px;color:var(--muted);margin:8px 0 46px;line-height:1.7;}
@media(max-width:768px){.spec-table{font-size:12.5px;}.spec-table th,.spec-table td{padding:9px 10px;}}
"""

for fn in ["exhaust-fan-sizes-guide.html", "commercial-kitchen-exhaust-fans.html"]:
    p = SITE + fn
    raw = open(p, "rb").read().decode("utf-8")
    if ".spec-table{" in raw:
        print(f"  skip {fn}: already has .spec-table")
        continue
    i = raw.find("</style>")
    if i < 0:
        print(f"  !! {fn}: no </style>")
        continue
    raw = raw[:i] + TBL_CSS + raw[i:]
    open(p, "wb").write(raw.encode("utf-8"))
    print(f"  ok {fn}: CSS injected at {i}")
print("done")
