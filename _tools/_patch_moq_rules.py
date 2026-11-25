# -*- coding: utf-8 -*-
p = '_tools/unify_moq_100_1125.py'
s = open(p, encoding='utf-8').read()
# Fix: و500 was mistyped as \u0642785 (\u0642 = ق, wrong); correct is \u0648500 (\u0648 = و + "500")
s = s.replace('\\u0642785', '\\u0648500')
# Fix: OEM custom-branding sentence actually contains "per model"
s = s.replace('MOQ 500 pcs for OEM with custom branding, higher for a new mould.',
              '500 pcs per model for OEM with custom branding, higher for a new mould.')
# Remove 2 redundant NO-HIT rules (already covered by other rules)
s = s.replace('    ("Minimum order is 500 pcs.",\n     "Minimum order is 100 pcs."),\n', '')
s = s.replace('    ("MOQ 500 pcs for OEM/custom, with mixed models in one container accepted.",\n     "MOQ 100 pcs per model for both stock and OEM/custom, with mixed models in one container accepted."),\n', '')
open(p, 'w', encoding='utf-8').write(s)
print('patched; remaining bad escape count =', s.count('\\u0642785'))
