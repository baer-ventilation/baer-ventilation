"""Fix口径 gaps found by 11-25 self-audit (Olivia decisions).
Idempotent, byte-level edit (site HTML is CRLF). Dry-run default; --apply to write.
"""
import sys, os

APPLY = '--apply' in sys.argv

# (file, old, new, note)  -- exact byte strings, CRLF preserved by bytes replace
RULES = [
    # 1. English f-desc legal name: earlier fix only touched zh dictionary
    ('js/main.js',
     b"Zhejiang Baer Electrical Technology Co., Ltd. is a professional ventilation supplier in Shengzhou, China.",
     b"Zhejiang Baer Electrical Technology Co.,ltd is a professional ventilation supplier in Shengzhou, China.",
     "EN f-desc legal name -> Co.,ltd"),

    # 2. foundingDate 2003 -> 2017-09-20 in Organization JSON-LD (en/zh about already fixed)
    ('verify/index.html',        b'"foundingDate": "2003"', b'"foundingDate": "2017-09-20"', "EN verify foundingDate"),
    ('zh/verify/index.html',     b'"foundingDate": "2003"', b'"foundingDate": "2017-09-20"', "ZH verify foundingDate"),
    ('ar/verify/index.html',     b'"foundingDate": "2003"', b'"foundingDate": "2017-09-20"', "AR verify foundingDate"),
    ('ar/about/index.html',      b'"foundingDate": "2003"', b'"foundingDate": "2017-09-20"', "AR about foundingDate"),

    # 3. Yemen MOQ a few hundred units -> 100 pcs (JSON-LD + visible FAQ)
    ('yemen-exhaust-fan-supplier.html',
     b'MOQ depends on the model - typically a few hundred units for standard wall and window fans, lower for larger inline and centrifugal units. Mixed containers are welcome. Send your model list and we will confirm exact MOQ and loading quantity.',
     b'MOQ is 100 pcs per model for both stock and OEM/custom. Mixed containers are welcome. Send your model list and we will confirm loading quantity.',
     "Yemen MOQ -> 100 pcs"),

    # 4. Visible employee stat 50-100 -> 51-100 (en dash); JSON-LD staff range aligned
    ('about/index.html',  b'<div class="num">50\xe2\x80\x93100</div>', b'<div class="num">51\xe2\x80\x93100</div>', "EN about employee stat"),
    ('zh/about/index.html', b'<div class="num">50\xe2\x80\x93100</div>', b'<div class="num">51\xe2\x80\x93100</div>', "ZH about employee stat"),
    ('baer-production-capacity.html',
     b'with 50\xe2\x80\x93100 staff and a 5-person export team',
     b'with 51-100 staff and a 5-person export team',
     "Capacity JSON-LD staff range"),
]

total = 0
for path, old, new, note in RULES:
    if not os.path.exists(path):
        print(f'[MISSING] {path}  ({note})')
        continue
    data = open(path, 'rb').read()
    n = data.count(old)
    total += n
    if n == 0:
        tag = 'SKIP(already fixed)' if new in data else 'NOT FOUND'
        print(f'[{tag}] {path}  ({note})')
        continue
    print(f'[HIT x{n}] {path}  ({note})')
    print('   OLD:', old.decode('utf-8', 'replace')[:110])
    print('   NEW:', new.decode('utf-8', 'replace')[:110])
    if APPLY:
        open(path, 'wb').write(data.replace(old, new))

print(f'\nTOTAL replacements: {total}   MODE: {"APPLY" if APPLY else "DRY-RUN"}')
