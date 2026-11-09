# -*- coding: utf-8 -*-
"""2026-11-09: 5 篇长指南首屏 At a Glance 摘要卡 + H2 锚点 id"""
import io, re

PAGES = {
    "exhaust-fan-sizes-guide.html": {
        "slugs": ["inch-vs-airflow","size-by-room","size-by-air-changes","measure-the-opening",
                  "why-airflow-differs","common-size-mistakes","specs-further-reading",
                  "certifications-factory","faq","send-room-size"],
        "h2tag": '<h2 class="sec">',
        "bullets": [
            'A &ldquo;6 inch exhaust fan&rdquo; can mean 150 m&sup3;/h or 1,670 m&sup3;/h &mdash; the inch is the mounting size, not the airflow.',
            'Size by room type and air changes per hour, then confirm the wall cut-out dimensions before ordering.',
            'The range runs from 4 inch bathroom fans to 18 inch panel fans &mdash; the full chart is below.'],
        "toc": [("inch-vs-airflow","The inch vs airflow"),("size-by-room","Which size for which room"),
                ("size-by-air-changes","Sizing by air changes"),("measure-the-opening","Measuring the opening"),
                ("why-airflow-differs","Why airflow differs"),("common-size-mistakes","5 common mistakes")],
    },
    "exhaust-fan-airflow-calculation-guide.html": {
        "slugs": ["measure-room-volume","choose-ach","apply-formula","unit-conversion","static-pressure",
                  "match-model","worked-example","common-sizing-mistakes","check-airflow-claim",
                  "need-help-sizing","market-application","related-guides","faq"],
        "h2tag": '<h2>',
        "bullets": [
            'Core formula: airflow = room volume &times; ACH &divide; 60 &mdash; a 3,000 ft&sup3; room at 8 ACH needs 400 CFM.',
            'Catalog airflow is measured at free air (0 Pa); ducts, bends and grilles cut real output, so budget for static pressure before matching a model.',
            'Unit conversion: CFM &times; 1.7 = m&sup3;/h, m&sup3;/h &divide; 1.7 = CFM &mdash; BAER spec sheets list both.'],
        "toc": [("measure-room-volume","1. Room volume"),("choose-ach","2. Choose ACH"),
                ("apply-formula","3. Apply the formula"),("unit-conversion","4. Convert units"),
                ("static-pressure","5. Static pressure"),("match-model","6. Match a model"),
                ("worked-example","Worked example"),("common-sizing-mistakes","Common mistakes")],
    },
    "exhaust-fan-noise-levels-guide.html": {
        "slugs": ["how-noise-measured","what-makes-quiet","keep-quiet","sones-vs-dba",
                  "noise-targets","read-datasheet","diagnose-noisy","faq"],
        "h2tag": '<h2>',
        "bullets": [
            'Below 35 dB(A) is quiet enough for a bedroom; 25&ndash;30 dB(A) is genuinely silent in practice.',
            'Datasheets quote sones or dB(A) &mdash; know both scales before comparing two fans.',
            'Many &ldquo;noisy fan&rdquo; complaints trace back to installation, not the fan &mdash; most are fixable after fitting.'],
        "toc": [("how-noise-measured","How noise is measured"),("what-makes-quiet","What makes a fan quiet"),
                ("keep-quiet","Keeping it quiet"),("sones-vs-dba","Sones vs dB(A)"),
                ("noise-targets","Targets by room"),("read-datasheet","Reading a datasheet"),
                ("diagnose-noisy","Diagnosing noise")],
    },
    "commercial-kitchen-exhaust-fans.html": {
        "slugs": ["grease-question","model-by-space","sizing-three-numbers","duct-velocity",
                  "pressure-budget","six-bxf-models","install-details","specs-further-reading",
                  "certifications-factory","faq","send-hood-length"],
        "h2tag": '<h2 class="sec">',
        "bullets": [
            'The first question is always grease: with a baffle filter fitted, the BXF mixed-flow range is the right tool.',
            'Sizing in three numbers: 100&ndash;300 CFM per linear foot of hood face by duty level, plus a 20% margin.',
            'The BXF range covers 290&ndash;2,200 m&sup3;/h at up to 693 Pa, factory-direct and CE certified.'],
        "toc": [("grease-question","Grease or not"),("model-by-space","Which model where"),
                ("sizing-three-numbers","Sizing: 3 numbers"),("duct-velocity","Duct velocity"),
                ("pressure-budget","Pressure budget"),("six-bxf-models","The six models"),
                ("install-details","Installation details")],
    },
    "exhaust-fan-maintenance-guide.html": {
        "slugs": ["failure-order","schedule-12-month","cleaning-by-family","four-checks",
                  "spare-parts","repair-or-replace","warranty-boundary","related-guides","need-spares"],
        "h2tag": '<h2 class="sec">',
        "bullets": [
            'Airflow loss and motor failure come last, not first &mdash; the early warning signs show up months ahead.',
            'A 12-month schedule, tightened for dusty, coastal or high-humidity sites.',
            'Warranty: 12 months on PP models, 24 months on ABS, against manufacturing defects &mdash; blocked impellers and hosing damage are not covered.'],
        "toc": [("failure-order","What fails first"),("schedule-12-month","12-month schedule"),
                ("cleaning-by-family","Cleaning by family"),("four-checks","Four early checks"),
                ("spare-parts","Spares to keep"),("repair-or-replace","Repair or replace"),
                ("warranty-boundary","Warranty boundary")],
    },
}

def card(cfg):
    lis = "".join("      <li>%s</li>\r\n" % b for b in cfg["bullets"])
    links = ' <span style="color:#CBD5E1;">&middot;</span> '.join(
        '<a href="#%s" style="color:#334155;text-decoration:none;border-bottom:1px solid #CBD5E1;">%s</a>' % (i, l)
        for i, l in cfg["toc"])
    return (
        '<div class="glance-card" style="background:var(--light);border:1px solid #E2E8F0;border-left:4px solid var(--red);border-radius:12px;padding:22px 26px;max-width:900px;margin:0 0 34px;">\r\n'
        '  <div style="font-size:12px;font-weight:700;letter-spacing:.14em;color:var(--red);text-transform:uppercase;margin-bottom:10px;">At a Glance</div>\r\n'
        '  <ul style="margin:0;padding-left:20px;font-size:15px;line-height:1.8;color:var(--dark);">\r\n'
        + lis +
        '  </ul>\r\n'
        '  <div style="margin-top:14px;padding-top:12px;border-top:1px solid #E2E8F0;font-size:13.5px;line-height:2;color:var(--text);"><strong style="color:var(--dark);">On this page:</strong> '
        + links + '</div>\r\n'
        '</div>\r\n')

CRLF = "\r\n"
for page, cfg in PAGES.items():
    raw = io.open(page, "rb").read().decode("utf-8")
    assert CRLF in raw, page

    # 1) H2 加 id（按出现顺序，兼容 class="sec" 与裸 h2）
    pat = re.compile(r'<h2( class="sec")?>')
    tags = list(pat.finditer(raw))
    assert len(tags) == len(cfg["slugs"]), f"{page}: h2 count {len(tags)} != slugs {len(cfg['slugs'])}"
    out, pos = [], 0
    for m, slug in zip(tags, cfg["slugs"]):
        cls = ' class="sec"' if m.group(1) else ''
        out.append(raw[pos:m.start()])
        out.append(f'<h2 id="{slug}"' + cls + '>')
        pos = m.end()
    out.append(raw[pos:])
    raw = "".join(out)

    # 2) 卡片插到首个 figure 之前
    fig = raw.find("<figure")
    assert fig > 0, page
    raw = raw[:fig] + card(cfg) + raw[fig:]

    assert 'class="glance-card"' in raw and f'id="{cfg["slugs"][0]}"' in raw
    io.open(page, "wb").write(raw.encode("utf-8"))
    print(f"OK {page}  h2_ids={len(cfg['slugs'])} toc={len(cfg['toc'])}")
