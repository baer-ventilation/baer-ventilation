# -*- coding: utf-8 -*-
"""Rebuild the container loading table / FAQ / worked example from the packing
data Olivia confirmed (Nov 2026)."""
import io, math, re, json

PACK = [
    ('KLT-10B', '6-inch', 20, 0.108, 18.05, 150),
    ('KLT-12B', '8-inch', 12, 0.142, 14.55, 380),
    ('KLT-18B', '10-inch', 10, 0.172, 16.00, 432),
    ('KLT-20B', '12-inch', 8, 0.189, 16.70, 792),
    ('KLT-25B', '14-inch', 4, 0.157, 12.50, 1500),
    ('KLT-30B', '18-inch', 1, 0.118, 6.25, 1800),
]
CONT = [('20GP', 28.2, 28200), ('40GP', 57.5, 26700), ('40HQ', 64.9, 26500)]


def loads(pcs, cbm, gw):
    out = []
    for name, vol, payload in CONT:
        by_vol = math.floor(vol / cbm)
        by_w = math.floor(payload / gw)
        n = min(by_vol, by_w)
        out.append((name, n * pcs, n, round(n * gw), 'volume' if by_vol <= by_w else 'weight'))
    return out


def n(v):
    return '{:,}'.format(v)


rows = []
for model, inch, pcs, cbm, gw, air in PACK:
    cells = ['<td><strong>%s %s</strong></td>' % (model, inch),
             '<td>%d / %.3g m³</td>' % (pcs, cbm),
             '<td>%d</td>' % air]
    for name, pieces, ctn, kg, lim in loads(pcs, cbm, gw):
        cells.append('<td>%s pcs<br><span style="color:#64748B;font-size:12.5px;">%s ctn · %s kg (%s-limited)</span></td>'
                     % (n(pieces), n(ctn), n(kg), lim))
    rows.append('      <tr>' + ''.join(cells) + '</tr>')

TABLE = '\n'.join(rows)
print(TABLE)

P = 'exhaust-fan-container-loading-guide.html'
s = io.open(P, encoding='utf-8', newline='').read()

# 1) replace the six data rows
start = s.index('<tr><td><strong>KLT-10B 6-inch</strong></td>')
end = s.index('</tbody>', start)
s = s[:start] + TABLE + '\n    ' + s[end:]

# 2) FAQ answers (visible + JSON-LD share the same sentence, replace globally)
faq = {
 'a20': ('It depends on the model. On our published packing data, a 20GP takes about 5,120 of the 6-inch KLT-10B, about 2,130 of the 8-inch KLT-12B, about 1,160 of the 12-inch KLT-20B, and about 258 of the 18-inch KLT-30B. Mixing sizes is accepted.',
         'It depends on the model. On our published packing data, a 20GP takes about 5,220 of the 6-inch KLT-10B, about 2,370 of the 8-inch KLT-12B, about 1,190 of the 12-inch KLT-20B, and about 238 of the 18-inch KLT-30B. Mixing sizes is accepted.'),
 'a40': ('Roughly double the 20GP figure for the same model — about 11,800 of the 6-inch KLT-10B, about 4,900 of the 8-inch KLT-12B, about 2,680 of the 12-inch KLT-20B and about 595 of the 18-inch KLT-30B, based on our standard export cartons.',
         'Roughly double the 20GP figure for the same model — about 12,000 of the 6-inch KLT-10B, about 5,470 of the 8-inch KLT-12B, about 2,740 of the 12-inch KLT-20B and about 550 of the 18-inch KLT-30B, based on our standard export cartons.'),
 'aw': ('Almost always by volume. On our packing data, every KLT model fills the container well before it approaches the weight limit — a 20GP of 6-inch fans comes to about 5,120 kg against a payload of roughly 28,200 kg.',
        'Almost always by volume. On our packing data, every KLT model fills the container well before it approaches the weight limit — a 20GP of 6-inch fans comes to about 4,710 kg against a payload of roughly 28,200 kg.'),
}
for k, (a, b) in faq.items():
    hits = s.count(a)
    print(k, 'hits', hits)
    s = s.replace(a, b)

# 3) worked example
ex = [
 ('<li>KLT-10B: 100 cartons × 0.110 m³ = 11.00 m³ → <strong>2,000 pcs</strong></li>',
  '<li>KLT-10B: 100 cartons × 0.108 m³ = 10.80 m³ → <strong>2,000 pcs</strong></li>'),
 ('<li>Volume remaining: 28.22 − 11.00 = <strong>17.22 m³</strong></li>',
  '<li>Volume remaining: 28.22 − 10.80 = <strong>17.42 m³</strong></li>'),
 ('<li>KLT-20B: 17.22 ÷ 0.145 = 118 cartons → <strong>708 pcs</strong></li>',
  '<li>KLT-20B: 17.42 ÷ 0.189 = 92 cartons → <strong>736 pcs</strong></li>'),
 ('<li>Total: <strong>2,708 pcs</strong> in 218 cartons, 28.11 m³, about 3,805 kg gross</li>',
  '<li>Total: <strong>2,736 pcs</strong> in 192 cartons, 28.19 m³, about 3,341 kg gross</li>'),
 ('Note what happened to the weight: 3,805 kg against a 28,200 kg payload.',
  'Note what happened to the weight: 3,341 kg against a 28,200 kg payload.'),
]
for a, b in ex:
    if a in s:
        s = s.replace(a, b)
    else:
        print('EX MISS', a[:60])

# 4) JSON-LD validity
for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
    json.loads(blk)

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('written')
