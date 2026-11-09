# -*- coding: utf-8 -*-
"""2026-11-09 实拍图铺页:社媒实拍转 webp,插入 9 个页面首个 H2 之前."""
import io, os
from PIL import Image

SRC = r"D:/WorkBuddy/2026-10-21-13-33-25/社媒素材_20261023"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMGDIR = os.path.join(ROOT, "images")
os.makedirs(IMGDIR, exist_ok=True)

# (源文件, 站点文件名, alt, caption, 目标页)
PLAN = [
    ("post05_fan_size_lineup.jpg", "fan-size-lineup.webp",
     "BAER inline duct fan size lineup from 4 inch to 12 inch",
     "The BAER inline duct family from 100 mm to 315 mm — the sizes this guide maps to rooms and duct runs.",
     "exhaust-fan-sizes-guide.html"),
    ("post02_motor_test_bench.jpg", "motor-test-bench.webp",
     "Motor test bench at the BAER factory measuring exhaust fan airflow and power",
     "Every BAER motor batch runs on a test bench before assembly — the rated airflow in the tables is measured, not estimated.",
     "exhaust-fan-airflow-calculation-guide.html"),
    ("alt_factory_assembly_line.jpg", "panel-fan-assembly-line.webp",
     "Panel exhaust fans on the BAER assembly line ready for testing",
     "Panel exhaust fans queued on the BAER assembly line — noise performance is checked per batch, not per catalogue claim.",
     "exhaust-fan-noise-levels-guide.html"),
    ("post06_shaft_qc_caliper.jpg", "shaft-qc-caliper.webp",
     "Digital caliper checking a fan motor shaft at BAER quality control",
     "Shaft and bearing checks at BAER QC — the same measurements that decide whether a worn fan can be serviced or should be replaced.",
     "exhaust-fan-maintenance-guide.html"),
    ("alt_factory_gate.jpg", "baer-factory-gate.webp",
     "BAER ventilation fan factory in Shengzhou Zhejiang China",
     "The BAER factory in Shengzhou, Zhejiang. Buyers are welcome to audit the lines before ordering — certificate scans are on our verification page.",
     "exhaust-fan-certifications-guide.html"),
    ("alt_container_loading.jpg", "container-loading.webp",
     "Exhaust fan export cartons loaded in a shipping container at the BAER factory",
     "Export cartons staged for container loading — SABER shipment documents are prepared per order for Saudi consignments.",
     "saber-saso-exhaust-fan-certification.html"),
    ("alt_assembly_workers.jpg", "assembly-workers.webp",
     "Workers assembling commercial kitchen exhaust fans at the BAER factory",
     "Commercial-duty exhaust fans in final assembly at the BAER factory in Zhejiang.",
     "commercial-kitchen-exhaust-fans.html"),
    ("post01_klt_series_lineup.jpg", "klt-series-lineup.webp",
     "KLT series panel exhaust fans with gravity auto-shutter as standard",
     "The KLT panel series ships with a gravity auto-shutter as standard on every model.",
     "exhaust-fan-shutter-types.html"),
    ("post04_industrial_inline_fan_controller.jpg", "inline-fan-controller.webp",
     "Inline duct fan speed controller inspected before packing at BAER",
     "Speed controller and capacitor box wired and function-checked before an inline fan ships.",
     "industrial-exhaust-fans.html"),
]

def crop_webp(src, dst, w=960, q=80):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    # 中心裁成 4:3
    tw, th = W, int(W * 3 / 4)
    if th > H:
        th, tw = H, int(H * 4 / 3)
    left, top = (W - tw) // 2, (H - th) // 2
    im = im.crop((left, top, left + tw, top + th)).resize((w, int(w * th / tw)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q)
    return im.size, os.path.getsize(dst) // 1024

def rd(p):
    with io.open(os.path.join(ROOT, p), "rb") as f:
        return f.read().decode("utf-8")

def wr(p, s):
    with io.open(os.path.join(ROOT, p), "wb") as f:
        f.write(s.encode("utf-8"))

for src, name, alt, cap, page in PLAN:
    size, kb = crop_webp(os.path.join(SRC, src), os.path.join(IMGDIR, name))
    t = rd(page)
    EOL = "\r\n" if "\r\n" in t else "\n"
    h2 = t.find("<h2")
    assert h2 > 0, f"{page}: no h2"
    # 若 h2 紧跟 section-tag span,回退到 span 之前
    tag = '<span class="section-tag"'
    tp = t.rfind(tag, 0, h2)
    if tp > 0 and t[tp:h2].find("<h2") >= 0 and t[tp:h2].count("</span>") >= 1 and t[tp:h2].count("<h2") == 1:
        h2 = tp
    fig = (
        '  <figure style="margin:26px 0;text-align:center;">' + EOL +
        f'    <img src="/images/{name}" alt="{alt}" width="{size[0]}" height="{size[1]}" '
        'loading="lazy" style="max-width:100%;height:auto;border-radius:8px;">' + EOL +
        f'    <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">{cap}</figcaption>' + EOL +
        "  </figure>" + EOL + EOL
    )
    t = t[:h2] + fig + t[h2:]
    assert f'images/{name}' in t
    wr(page, t)
    print(f"{page:46s} <- {name:30s} {size[0]}x{size[1]} {kb}KB")

print("IMAGES DONE")
