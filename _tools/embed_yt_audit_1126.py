"""Embed published YouTube video on audit-checklist page + VideoObject + dateModified + sitemap lastmod.
Idempotent, byte-level (page is CRLF). Dry-run default; --apply to write.
Video ID xNDkLVF9maE, published 2026-11-26, verified via oEmbed 200.
"""
import sys, os
APPLY = '--apply' in sys.argv
PAGE = 'exhaust-fan-supplier-audit-checklist.html'
VID = 'xNDkLVF9maE'

VIDEO_JSONLD = '''<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"VideoObject",
  "name":"Exhaust Fan Supplier Audit: 30-Point Scorecard | BAER",
  "description":"30-point exhaust fan supplier audit scorecard: six groups, eight photos to request from the factory floor and ten red flags. Score each line 0 / 1 / 2; below 35 out of 60 keep the order at sample stage. Companion to the BAER supplier audit checklist.",
  "thumbnailUrl":["https://i.ytimg.com/vi/xNDkLVF9maE/hqdefault.jpg"],
  "uploadDate":"2026-11-26T07:30:00+08:00",
  "duration":"PT3M30S",
  "embedUrl":"https://www.youtube.com/embed/xNDkLVF9maE",
  "contentUrl":"https://youtu.be/xNDkLVF9maE",
  "publisher":{"@type":"Organization","name":"BAER Ventilation","legalName":"Zhejiang Baer Electrical Technology Co.,ltd","url":"https://baer-ventilation.com"}
}
</script>
'''

IFRAME = '''<figure style="margin:26px 0;text-align:center;">
  <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:860px;margin:0 auto;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.18);"><iframe src="https://www.youtube.com/embed/xNDkLVF9maE" title="Exhaust Fan Supplier Audit: 30-Point Scorecard | BAER" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" loading="lazy" allowfullscreen></iframe></div>
  <figcaption style="font-size:12.5px;color:#64748b;margin-top:8px;">Watch: how to run the 30-point supplier audit before you release a deposit</figcaption>
</figure>
'''

# (file, old, new, note)
RULES = [
    # 1. Append VideoObject after the FAQ JSON-LD block (anchor: end of FAQ page script)
    (PAGE,
     b'}</script>\n<style>',
     b'}</script>\n' + VIDEO_JSONLD.encode() + b'\n<style>',
     'append VideoObject before <style>'),

    # 2. Insert iframe figure before the first factory-gate figure in body
    (PAGE,
     b'<figure style="margin:26px 0;text-align:center;">\n    <img src="/images/baer-factory-gate.webp"',
     IFRAME.encode() + b'<figure style="margin:26px 0;text-align:center;">\n    <img src="/images/baer-factory-gate.webp"',
     'insert video embed before factory-gate figure'),

    # 3. Update JSON-LD dateModified
    (PAGE,
     b'"dateModified":"2026-11-23"',
     b'"dateModified":"2026-11-26"',
     'WebPage dateModified'),

    # 4. Update visible Last updated
    (PAGE,
     b'Last updated: November 23, 2026',
     b'Last updated: November 26, 2026',
     'visible Last updated'),

    # 5. sitemap lastmod for this URL only (loc followed by lastmod)
    ('sitemap.xml',
     b'<loc>https://baer-ventilation.com/exhaust-fan-supplier-audit-checklist</loc>\n    <lastmod>2026-11-23</lastmod>',
     b'<loc>https://baer-ventilation.com/exhaust-fan-supplier-audit-checklist</loc>\n    <lastmod>2026-11-26</lastmod>',
     'sitemap lastmod'),
]

def crlf(b):
    """normalize literal \n in rule bytes to CRLF, matching the on-disk files."""
    return b.replace(b'\n', b'\r\n')

IFRAME_MARK = b'<iframe src="https://www.youtube.com/embed/' + VID.encode() + b'"'

total = 0
for path, old, new, note in RULES:
    data = open(path, 'rb').read()
    old, new = crlf(old), crlf(new)
    # guard: video embed rule must check the iframe itself, not the video id
    # (the id also appears inside the VideoObject JSON-LD)
    if note.startswith('insert video embed') and IFRAME_MARK in data:
        print(f'[SKIP(already embedded)] {path} ({note})')
        continue
    n = data.count(old)
    if n == 0:
        tag = 'SKIP(already done)' if new in data else 'NOT FOUND'
        print(f'[{tag}] {path} ({note})')
        # for append rules, check idempotency by marker
        if note.startswith('append') and VID.encode() in data:
            print('   video id marker present -> already embedded')
        continue
    if n != 1:
        print(f'[AMBIGUOUS x{n}] {path} ({note}) -- aborting this rule')
        continue
    total += 1
    print(f'[HIT x1] {path} ({note})')
    if APPLY:
        open(path, 'wb').write(data.replace(old, new, 1))

print(f'\nTOTAL changes: {total}  MODE: {"APPLY" if APPLY else "DRY-RUN"}')
