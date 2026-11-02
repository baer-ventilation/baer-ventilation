# -*- coding: utf-8 -*-
"""Update KLT packing data to the figures Olivia confirmed in the B2B data sheet.
Pcs/Ctn, CBM, G.W. replaced; N.W. column removed (net weight depends on motor
winding / cable / plug and is confirmed on the packing list).
"""
import io, os, re, sys

NEW = {
    '10B': dict(pcs=20, cbm='0.108', gw='18.05'),
    '12B': dict(pcs=12, cbm='0.142', gw='14.55'),
    '18B': dict(pcs=10, cbm='0.172', gw='16.00'),
    '20B': dict(pcs=8,  cbm='0.189', gw='16.70'),
    '25B': dict(pcs=4,  cbm='0.157', gw='12.50'),
    '30B': dict(pcs=1,  cbm='0.118', gw='6.25'),
}
# old values currently published, keyed by model
OLD = {
    '10B': dict(pcs=20, cbm='0.11', gw='20', nw='19'),
    '12B': dict(pcs=9,  cbm='0.119', gw='12.8', nw='11.8'),
    '18B': dict(pcs=8,  cbm='0.168', gw='17.5', nw='16.5'),
    '20B': dict(pcs=6,  cbm='0.145', gw='15.3', nw='14.3'),
    '25B': dict(pcs=4,  cbm='0.146', gw='13.5', nw='12.8'),
    '30B': dict(pcs=1,  cbm='0.109', gw='6.3', nw='5.7'),
}

FILES = [
    'klt-series-panel-exhaust-fan.html',
    'product-klt-10b.html', 'product-klt-12b.html', 'product-klt-18b.html',
    'product-klt-20b.html', 'product-klt-25b.html', 'product-klt-30b.html',
    'ar/product-klt-10b.html', 'zh/product-klt-10b.html',
]

CELL = re.compile(r'<td>\d+ pcs/ctn</td><td>[\d.]+ m³</td><td>[\d.]+ kg</td><td>[\d.]+ kg</td>')
TBL = re.compile(r'<table class="spec-table">.*?</table>', re.S)


def fmt(v):
    return v


def patch_table(block, counts):
    out = block
    for m, v in NEW.items():
        row = re.compile(
            r'(<td>KLT-%s[^<]*</td>(?:(?!</tr>).)*?)' % m + CELL.pattern, re.S)
        new_cells = '<td>%d pcs/ctn</td><td>%s m³</td><td>%s kg</td>' % (v['pcs'], v['cbm'], v['gw'])
        out, n = row.subn(lambda mm: mm.group(1) + new_cells, out)
        counts[m] = counts.get(m, 0) + n
    # drop the N.W. header (English / Arabic / Chinese variants)
    before = out
    out = out.replace('<th>N.W.</th>', '')
    out = out.replace('<th>الوزن الصافي</th>', '')
    out = out.replace('<th>净重</th>', '')
    if out != before:
        counts['nw_header'] = counts.get('nw_header', 0) + 1
    # drop the duplicate (Kg/Ctn) unit header
    out2, n2 = re.subn(r'(<th class="unit">\(Kg/[^<]*\)</th>)<th class="unit">\(Kg/[^<]*\)</th>', r'\1', out)
    if n2:
        counts['nw_unit_header'] = counts.get('nw_unit_header', 0) + n2
        out = out2
    return out


def main():
    for p in FILES:
        if not os.path.exists(p):
            print('MISSING', p); continue
        s = io.open(p, encoding='utf-8', newline='').read()
        counts = {}
        s = TBL.sub(lambda m: patch_table(m.group(0), counts) if 'KLT-10B' in m.group(0) else m.group(0), s)

        # product detail (2-column) rows + prose, per file
        mt = re.search(r'product-klt-(\d\d)b\.html', p)
        if mt and '/ar/' not in p and '/zh/' not in p:
            k = mt.group(1) + 'B'
            o, v = OLD[k], NEW[k]
            reps = [
                ('<tr><td>Packing</td><td>%d pcs/ctn</td></tr>' % o['pcs'],
                 '<tr><td>Packing</td><td>%d pcs/ctn</td></tr>' % v['pcs']),
                ('<tr><td>Volume per carton</td><td>%s m³</td></tr>' % o['cbm'],
                 '<tr><td>Volume per carton</td><td>%s m³</td></tr>' % v['cbm']),
                ('<tr><td>Gross / net weight</td><td>%s kg / %s kg per carton</td></tr>' % (o['gw'], o['nw']),
                 '<tr><td>Gross weight</td><td>%s kg per carton</td></tr>' % v['gw']),
                ('with %d pcs/ctn' % o['pcs'], 'with %d pcs/ctn' % v['pcs']),
            ]
            for a, b in reps:
                if a in s:
                    s = s.replace(a, b); counts['detail'] = counts.get('detail', 0) + 1
                else:
                    print('  detail MISS', os.path.basename(p), a[:60])

        if '/zh/' in p:
            a = '出口包装 20 pcs/箱（体积 0.11 m³，毛重 20 kg）'
            b = '出口包装 20 pcs/箱（体积 0.108 m³，毛重 18.05 kg）'
            if a in s:
                s = s.replace(a, b); counts['prose'] = 1
        if '/ar/' in p:
            a = '(حجم 0.11 m³، وزن قائم 20 كجم)'
            b = '(حجم 0.108 m³، وزن قائم 18.05 كجم)'
            if a in s:
                s = s.replace(a, b); counts['prose'] = 1

        io.open(p, 'w', encoding='utf-8', newline='').write(s)
        print(p, counts)


if __name__ == '__main__':
    main()
