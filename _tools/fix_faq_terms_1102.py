import io, re, sys

P = "faq.html"
with io.open(P, "r", encoding="utf-8", newline="") as f:
    s = f.read()

orig = s
reps = []

# ---- 1) Sample answer (HTML) ----
reps.append((
 '<div class="ans">Yes. We ship single-unit samples for evaluation, freight collect (Samples available — freight collect). The sample fee is usually credited back against your first bulk order.</div>',
 '<div class="ans">Yes. We supply single-unit samples for evaluation. Samples are <strong>charged</strong> (sample fee applies) and <strong>freight is paid by the buyer</strong>. Send us the model, quantity and your destination — or your courier account — and we will confirm the sample cost and shipping charge the same day.</div>'
))

# ---- 1b) Sample answer (JSON-LD) ----
reps.append((
 '"text": "Yes. We ship single-unit samples for evaluation, freight collect. The sample fee is usually credited back against your first bulk order."',
 '"text": "Yes. We supply single-unit samples for evaluation. Samples are charged (a sample fee applies) and freight is paid by the buyer. Send us the model, quantity and destination and we will confirm sample cost and shipping the same day."'
))

# ---- 2) Lead time (HTML) ----
reps.append((
 '<div class="ans">Standard in-stock models: <strong>3–7 days</strong>. Standard production orders: <strong>20–30 days</strong>. OEM/custom mold orders: <strong>45–60 days</strong> (including tooling). We provide weekly production updates and pre-shipment photos.</div>',
 '<div class="ans">Bulk production (standard models): <strong>25–35 days</strong> from receipt of deposit and confirmed artwork. Stock items can ship faster — ask us to check current inventory. OEM/custom tooling orders: <strong>45–60 days</strong> including mould development. We send weekly production updates and pre-shipment photos.</div>'
))

# ---- 2b) Lead time (JSON-LD) ----
reps.append((
 '"text": "Standard in-stock models: 3\u20137 days. Standard production: 20\u201330 days. OEM/custom: 45\u201360 days."',
 '"text": "Bulk production for standard models takes 25\u201335 days from receipt of deposit and confirmed artwork. Stock items can ship faster. OEM/custom tooling orders take 45\u201360 days including mould development."'
))

# ---- 3) Packaging (HTML) ----
reps.append((
 '<div class="ans">Each fan is packed in an individual carton with foam or EPS protection, then loaded on export pallets or into reinforced cartons for container shipping. We send pre-shipment packing photos before every shipment.</div>',
 '<div class="ans">Default packing is an individual <strong>neutral kraft carton</strong> with foam or EPS protection — no branding, which keeps your options open. From <strong>1,000 pcs per model</strong> we print your <strong>custom colour box free of charge</strong>. Export <strong>pallets are available on request at extra cost</strong>. We send pre-shipment packing photos before every shipment.</div>'
))

# ---- 3b) Packaging (JSON-LD) ----
reps.append((
 '"text": "Each fan is packed in an individual carton with foam or EPS protection, then palletised for container shipping."',
 '"text": "Default packing is an individual neutral kraft carton with foam or EPS protection. From 1,000 pcs per model we print a custom colour box free of charge. Export pallets are available on request at extra cost."'
))

# ---- 4) Payment terms: make 30/70 and L/C explicit (HTML) ----
reps.append((
 '<div class="ans">We accept <strong>T/T (bank transfer)</strong>, <strong>L/C at sight</strong>, and Western Union. Standard terms: 30% deposit, 70% before shipment. For long-term partners, we offer flexible arrangements.</div>',
 '<div class="ans">Standard terms are <strong>30% T/T deposit and 70% balance before shipment</strong>. We also accept <strong>L/C at sight</strong> and Western Union. For repeat and long-term partners we can discuss more flexible arrangements.</div>'
))

# ---- 4b) Payment (JSON-LD) ----
reps.append((
 '"text": "We accept T/T, L/C at sight, and Western Union. Standard terms: 30% deposit, 70% before shipment."',
 '"text": "Standard terms are 30% T/T deposit and 70% balance before shipment. We also accept L/C at sight and Western Union."'
))

# ---- 5) dateModified ----
reps.append(('"dateModified": "2026-10-27"', '"dateModified": "2026-11-02"'))

miss = []
for old, new in reps:
    if old not in s:
        miss.append(old[:70])
    else:
        s = s.replace(old, new, 1)

if miss:
    print("MISSING:")
    for m in miss:
        print("  -", m)
    sys.exit(1)

# count rendered questions
n_items = len(re.findall(r'<div class="faq-item">', s))
print("faq-item count:", n_items)

with io.open(P, "w", encoding="utf-8", newline="") as f:
    f.write(s)
print("OK, changed bytes:", len(s) - len(orig))
