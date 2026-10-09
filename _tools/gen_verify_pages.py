# -*- coding: utf-8 -*-
"""
生成 /verify/ 三语页面（EN 可索引 / AR 可索引 / ZH noindex）。
- 复用 about 页的 head 引导脚本、navbar、about 式居中页脚
- JSON-LD 与同语言 about 页同构：blockA(mainEntity Organization) + blockB(WebPage + BreadcrumbList)
- 输出到 ./verify/index.html, ./ar/verify/index.html, ./zh/verify/index.html
用法：python gen_verify_pages.py [--apply]   （不带 --apply 只干跑并打印摘要）
"""
import io, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONT = ""  # 无需额外字体

CSS_COMMON = """  body{padding-top:var(--nav-h);}
  .page-hero{background:linear-gradient(135deg,#0F172A 0%,#1E293B 100%);color:#fff;padding:72px 0 60px;text-align:center;}
  .page-hero h1{color:#fff !important;font-size:40px;font-weight:900;letter-spacing:-1px;margin-bottom:14px;text-shadow:0 2px 8px rgba(0,0,0,.25);}
  .page-hero p{color:#CBD5E1;font-size:17px;max-width:760px;margin:0 auto;}
  .section{padding:64px 0;}
  .section.alt{background:var(--baer-light);}
  .sec-title{font-size:28px;font-weight:800;color:var(--baer-dark);margin-bottom:10px;text-align:center;}
  .sec-sub{color:var(--baer-gray);text-align:center;margin-bottom:38px;font-size:15px;max-width:820px;margin-left:auto;margin-right:auto;}
  .grid-2{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:26px;max-width:980px;margin:0 auto;}
  .card{background:#fff;border:1px solid #E2E8F0;border-radius:var(--radius);padding:26px;transition:box-shadow .25s ease,transform .25s ease;}
  .card:hover{box-shadow:var(--shadow);transform:translateY(-3px);}
  .entity{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:24px;box-shadow:0 4px 16px rgba(15,23,42,.05);}
  .entity .role{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#fff;background:var(--baer-red,#E21E26);padding:4px 11px;border-radius:20px;margin-bottom:12px;}
  .entity h3{margin:0 0 10px;font-size:18px;font-weight:900;color:#0F172A;line-height:1.35;}
  .entity dl{margin:0;font-size:14px;}
  .entity dt{font-weight:800;color:#475569;margin-top:11px;font-size:12px;letter-spacing:.4px;text-transform:uppercase;}
  .entity dd{margin:3px 0 0;color:#1E293B;line-height:1.6;}
  .vid{font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:700;color:#B91C1C;word-break:break-all;letter-spacing:.3px;}
  .vtable{width:100%;border-collapse:collapse;font-size:14px;max-width:1000px;margin:0 auto;}
  .vtable th{background:#0F172A;color:#fff;text-align:left;padding:12px 14px;font-size:13px;letter-spacing:.3px;}
  .vtable td{padding:12px 14px;border-bottom:1px solid #E2E8F0;vertical-align:top;line-height:1.55;}
  .vtable tr:nth-child(even) td{background:#F8FAFC;}
  .vtable a{color:#B91C1C;word-break:break-all;}
  .alert{background:#FFF5F5;border-left:5px solid #E21E26;border-radius:0 10px 10px 0;padding:24px 26px;margin:0 auto 24px;max-width:1000px;box-shadow:0 4px 16px rgba(226,30,38,.08);}
  .alert .lbl{font-size:12px;font-weight:800;letter-spacing:1px;text-transform:uppercase;color:#991B1B;margin-bottom:6px;}
  .alert .bn{font-size:21px;font-weight:900;color:#991B1B;letter-spacing:.4px;word-break:break-word;line-height:1.3;}
  .alert p{color:#7F1D1D;font-size:14px;margin:12px 0 0;line-height:1.7;}
  ul.rules{list-style:none;padding:0;margin:22px auto 0;max-width:1000px;}
  ul.rules li{padding:11px 0 11px 30px;position:relative;color:#475569;font-size:15px;line-height:1.7;border-bottom:1px dashed #E2E8F0;}
  ul.rules li::before{content:"\\26A0";position:absolute;left:0;top:10px;color:#E21E26;font-weight:900;}
  ul.rules li strong{color:#0F172A;}
  ul.steps{counter-reset:s;list-style:none;padding:0;margin:22px auto 0;max-width:1000px;}
  ul.steps li{counter-increment:s;padding:12px 0 12px 46px;position:relative;color:#475569;font-size:15px;line-height:1.7;}
  ul.steps li::before{content:counter(s);position:absolute;left:0;top:11px;width:30px;height:30px;border-radius:50%;background:#E21E26;color:#fff;font-weight:800;font-size:14px;display:flex;align-items:center;justify-content:center;}
  .note{background:#F1F5F9;border-radius:10px;padding:18px 22px;max-width:1000px;margin:22px auto 0;color:#475569;font-size:14px;line-height:1.75;}
  .cta-band{background:linear-gradient(135deg,#0F172A,#1E293B);color:#fff;padding:56px 0;text-align:center;}
  .cta-band h2{font-size:28px;font-weight:900;margin-bottom:10px;color:#fff;}
  .cta-band p{color:#CBD5E1;margin-bottom:24px;max-width:720px;margin-left:auto;margin-right:auto;}
  .cta-actions{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
  .baer-btn-v2{display:inline-block;background:var(--baer-red,#E21E26);color:#fff;padding:14px 30px;border-radius:6px;font-weight:800;font-size:15px;letter-spacing:.5px;text-decoration:none;transition:background .25s ease,transform .2s ease;}
  .baer-btn-v2:hover{background:#C01820;transform:translateY(-2px);}
  .btn-ghost{display:inline-block;border:2px solid var(--baer-red,#E21E26);color:#fff;padding:12px 26px;border-radius:6px;font-weight:800;font-size:14px;text-decoration:none;transition:all .25s ease;}
  .btn-ghost:hover{background:#E21E26;}
  .updated{text-align:center;color:#94A3B8;font-size:13px;margin-top:14px;}
  [dir="rtl"] .alert{border-left:0;border-right:5px solid #E21E26;border-radius:10px 0 0 10px;}
  [dir="rtl"] ul.rules li{padding:11px 30px 11px 0;}
  [dir="rtl"] ul.rules li::before{left:auto;right:0;}
  [dir="rtl"] ul.steps li{padding:12px 46px 12px 0;}
  [dir="rtl"] ul.steps li::before{left:auto;right:0;}
  @media(max-width:768px){ .page-hero h1{font-size:28px;} .vtable{font-size:12px;} .vtable th,.vtable td{padding:9px;} }"""

BC_CSS = """.baer-breadcrumb{font-size:13px;line-height:1.6;margin:0 0 14px;letter-spacing:.2px;}
.baer-breadcrumb ol{list-style:none;display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:0;padding:0;}
.baer-breadcrumb li{display:inline-flex;align-items:center;gap:6px;color:inherit;opacity:.75;}
.baer-breadcrumb li:last-child{opacity:1;font-weight:600;}
.baer-breadcrumb a{color:inherit;text-decoration:none;border-bottom:1px solid transparent;}
.baer-breadcrumb a:hover{border-bottom-color:currentColor;}
.baer-breadcrumb .sep{opacity:.45;font-size:12px;}
.baer-breadcrumb[dir="rtl"] ol{flex-direction:row-reverse;justify-content:flex-end;}"""

GTM = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y7GNF2D0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0Y7GNF2D0H');
</script>
<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "y7asoc678j");
</script>"""

SAME_AS = ["https://www.youtube.com/@BAERVentilation",
           "https://www.linkedin.com/company/baer-ventilation",
           "https://discovery.patsnap.com/company/zhejiang-baer-electrical-technology",
           "https://www.qixin.com/company/46a65271-58ea-4791-bc97-10681bc264f6",
           "https://www.tradewheel.com/co/zhejiang-baer-appliance-technology-co-1040399"]

ORG = {
    "@type": "Organization",
    "@id": "https://baer-ventilation.com/#organization",
    "name": "BAER Ventilation",
    "legalName": "Zhejiang Baer Electrical Technology Co., Ltd.",
    "sameAs": SAME_AS,
    "foundingDate": "2003",
    "numberOfEmployees": {"@type": "QuantitativeValue", "minValue": 50, "maxValue": 100},
    "email": "sunny@zjbaer.com",
    "telephone": "+8613655859122",
    "address": {"@type": "PostalAddress", "streetAddress": "8-1 Jingwu Road, Ganlin Town, Shengzhou City",
                "addressLocality": "Shaoxing", "addressRegion": "Zhejiang", "postalCode": "312400", "addressCountry": "CN"},
}

# ---------- 三语内容 ----------
C = {}
C['en'] = dict(
    lang='en', dir='ltr', robots=None,
    title="Verify BAER Ventilation | Company, Certificates & Bank Beneficiary",
    desc="Verify the legal identity, ISO 9001 / CCC / CE certificates and bank beneficiary name of BAER Ventilation (Zhejiang Baer Electrical Technology Co., Ltd.) before you order or wire money.",
    og_locale='en_US',
    nav=[("/", "Home"), ("/products/", "Products"), ("/about/", "About"), ("/resources", "Resources"), ("/contact/", "Contact")],
    langbtn="EN", langlinks=[("https://baer-ventilation.com/verify/", "EN"), ("https://baer-ventilation.com/zh/verify/", "中文"), ("https://baer-ventilation.com/ar/verify/", "العربية")],
    h1="Verify BAER Ventilation",
    hero="Check our legal identity, certificates and bank beneficiary — before you place an order or send payment.",
    crumbs=[("/", "Home"), (None, "Verify Our Company")],
    s1t="Who You Are Dealing With",
    s1s="BAER Ventilation is a factory group. Your contract and payment go to our wholly-owned export company — here are both legal entities, so you can check them on the official registry.",
    e1_role="Manufacturing entity",
    e1_name="Zhejiang Baer Electrical Technology Co., Ltd.",
    e1_rows=[("Unified Social Credit Code", "91330683MA29E0KR3C"),
             ("Legal representative", "Lu Fengping (吕锋平)"),
             ("Registered address", "No. 8-1 Jingwu Road, Ganlin Town, Shengzhou City, Shaoxing, Zhejiang 312400, China"),
             ("Established", "2017 (factory roots since 2003)"),
             ("Role", "Manufacturing, QC, injection moulding, motor winding, product certification")],
    e2_role="Export & payment entity",
    e2_name="SHAOXING BAER IMPORT & EXPORT CO., LTD.",
    e2_rows=[("Unified Social Credit Code", "91330683MA2JQPJT6U"),
             ("Legal representative", "Lu Fengping (吕锋平) — same person"),
             ("Registered address", "Floor 6, Building 3, Zhichuang Park, No. 3 Lingdaiyuan 2nd Road, Sanjiang Street, Shengzhou City, Shaoxing, Zhejiang, China"),
             ("Established", "2020"),
             ("Customs registration", "Registered 2020-12-04 with Shaoxing Customs as importer/exporter of record (valid to 2068)"),
             ("Role", "Contracts, proforma invoices, export documents and payment collection")],
    rel_note="<strong>Relationship:</strong> Shaoxing Baer Import &amp; Export Co., Ltd. is a 100% wholly-owned subsidiary of Zhejiang Baer Electrical Technology Co., Ltd. Both share the same legal representative. This is a standard structure for Chinese manufacturers — the factory manufactures, and its own export company signs contracts and collects payment.",
    gsxt_title="How to verify us on the official registry",
    gsxt_steps=[
        "Open the <strong>National Enterprise Credit Information Publicity System (GSXT)</strong>: <a href=\"https://www.gsxt.gov.cn\" target=\"_blank\" rel=\"noopener\">https://www.gsxt.gov.cn</a>",
        "Enter our Unified Social Credit Code — <span class=\"vid\">91330683MA29E0KR3C</span> (factory) or <span class=\"vid\">91330683MA2JQPJT6U</span> (export company).",
        "Confirm the company name, legal representative and registered address match this page.",
    ],
    s2t="Certificates You Can Verify",
    s2s="Every certificate below can be checked against the issuing body or a government platform. The certificate images are shown on our About page.",
    t_head=["Certificate", "Number", "Issuer", "Valid until", "Where to verify"],
    t_rows=[
        ["ISO 9001:2015 — Quality Management System", "<span class=\"vid\">04625Q15304R1M</span>",
         "Beijing Head International Certification Co., Ltd. (CNAS C046-M)", "2028-11-16",
         "CNCA platform: <a href=\"https://cx.cnca.cn\" target=\"_blank\" rel=\"noopener\">cx.cnca.cn</a> (enter the certificate number)"],
        ["CCC — China Compulsory Certification", "<span class=\"vid\">2024010702612682</span>",
         "China Quality Certification Centre (CQC)", "2029-03-11",
         "CQC: <a href=\"http://www.cqc.com.cn\" target=\"_blank\" rel=\"noopener\">www.cqc.com.cn</a> / CNCA platform"],
        ["CE — EMC Directive 2014/30/EU", "<span class=\"vid\">XH2601E0321945GC</span> (test report <span class=\"vid\">XH2601E0321945GR</span>)",
         "XHIT — Xhiua International Testing &amp; Certification (Shenzhen) Co., Ltd.", "—",
         "Issuer: <a href=\"https://www.xhit-lab.com\" target=\"_blank\" rel=\"noopener\">www.xhit-lab.com</a>"],
        ["CB Scheme — safety test report (IEC 60335-2-80)", "Report No. <span class=\"vid\">60444427 001</span>",
         "TÜV Rheinland (LCIE originator)", "—", "Report available on request"],
    ],
    t_note="For the CB Scheme we currently hold the accredited TÜV Rheinland test report; a full CB Test Certificate can be arranged on request. Test reports and certificate scans are sent with every quotation.",
    s3t="Bank Beneficiary &amp; Payment Safety",
    s3s="This is the name that must appear on your wire transfer. Anything else is not us.",
    bn_label="Official payment beneficiary name",
    bn="SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.",
    bn_note="Bank name, account number and SWIFT code are printed on your Proforma Invoice / contract only. We never send them from a free mailbox, and we never change them without a live video call.",
    rules=[
        "<strong>If an email says our bank details changed — stop.</strong> Do not pay. Confirm with us first by video call or a known phone number.",
        "Check the beneficiary name on your PI matches <strong>SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.</strong> exactly — no other company or personal name.",
        "<strong>We never</strong> ask for payment to a personal account or to a third-party company.",
        "Cross-check every document against the codes and certificate numbers listed on this page.",
    ],
    s4t="Factory Audit &amp; Live Video Tour",
    s4s="Prefer to see it yourself? We host live video factory tours and can share third-party inspection reports, production capacity and export records for your due diligence.",
    cta_h="Ready to verify and order?",
    cta_p="Send your requirements — ask for certificates, a video tour or a factory audit report together with your quotation.",
    cta_a="/contact/", cta_at="Request a Quote",
    cta_b="/baer-fan-catalog.pdf", cta_bt="Download Catalog PDF",
    updated="Last updated: October 9, 2026",
    footer_desc="Exhaust fan manufacturer & exporter · Middle East, Europe, North America",
    footer_verify="Verify Our Company", footer_priv="Privacy Policy", footer_cookie="Cookie Notice",
    bc_home="Home", bc_name="Verify Our Company",
)

C['ar'] = dict(
    lang='ar', dir='rtl', robots=None,
    title="تحقّق من BAER Ventilation | الهوية القانونية والشهادات وحساب الدفع",
    desc="تحقّق من الهوية القانونية وشهادات ISO 9001 وCCC وCE واسم المستفيد البنكي لشركة BAER Ventilation (Zhejiang Baer Electrical Technology Co., Ltd.) قبل الطلب أو التحويل.",
    og_locale='ar_AE',
    nav=[("/ar/", "الرئيسية"), ("/ar/products/", "المنتجات"), ("/ar/about/", "من نحن"), ("/resources", "المصادر"), ("/ar/contact/", "اتصل بنا")],
    langbtn="العربية", langlinks=[("https://baer-ventilation.com/verify/", "EN"), ("https://baer-ventilation.com/zh/verify/", "中文"), ("https://baer-ventilation.com/ar/verify/", "العربية")],
    h1="تحقّق من BAER Ventilation",
    hero="تحقّق من هويتنا القانونية وشهاداتنا واسم المستفيد البنكي — قبل الطلب أو إرسال الدفعة.",
    crumbs=[("/ar/", "الرئيسية"), (None, "تحقّق من شركتنا")],
    s1t="مع من تتعامل",
    s1s="BAER Ventilation مجموعة مصنعية. العقد والدفع يتمّان عبر شركة التصدير المملوكة بالكامل لنا — وفيما يلي الكيانان القانونيان لتتحقق منهما في السجل الرسمي.",
    e1_role="الكيان المُصنّع",
    e1_name="Zhejiang Baer Electrical Technology Co., Ltd.",
    e1_rows=[("رمز الائتمان الاجتماعي الموحّد", "91330683MA29E0KR3C"),
             ("الممثل القانوني", "Lu Fengping (吕锋平)"),
             ("العنوان المسجّل", "No. 8-1 Jingwu Road, Ganlin Town, Shengzhou City, Shaoxing, Zhejiang 312400, China"),
             ("سنة التأسيس", "2017 (جذور المصنع منذ 2003)"),
             ("الدور", "التصنيع ومراقبة الجودة والحقن ولفّ المحركات وشهادات المنتج")],
    e2_role="كيان التصدير والدفع",
    e2_name="SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.",
    e2_rows=[("رمز الائتمان الاجتماعي الموحّد", "91330683MA2JQPJT6U"),
             ("الممثل القانوني", "Lu Fengping (吕锋平) — نفس الشخص"),
             ("العنوان المسجّل", "Floor 6, Building 3, Zhichuang Park, No. 3 Lingdaiyuan 2nd Road, Sanjiang Street, Shengzhou City, Shaoxing, Zhejiang, China"),
             ("سنة التأسيس", "2020"),
             ("تسجيل الجمارك", "مسجّلة بتاريخ 2020-12-04 لدى جمارك شاوشينغ كمستورد/مصدّر (سارية حتى 2068)"),
             ("الدور", "العقود والفواتير الأولية ومستندات التصدير وتحصيل الدفعات")],
    rel_note="<strong>العلاقة:</strong> شركة Shaoxing Baer Import &amp; Export مملوكة بنسبة 100% لشركة Zhejiang Baer Electrical Technology، ويشترك الكيانان في نفس الممثل القانوني. وهذا هيكل معتاد لدى المصانع الصينية — المصنع يُنتج، وشركة التصدير الخاصة به توقّع العقود وتحصّل الدفعات.",
    gsxt_title="كيف تتحقّق منّا في السجل الرسمي",
    gsxt_steps=[
        "افتح <strong>النظام الوطني للإفصاح عن معلومات الائتمان للمؤسسات (GSXT)</strong>: <a href=\"https://www.gsxt.gov.cn\" target=\"_blank\" rel=\"noopener\">https://www.gsxt.gov.cn</a>",
        "أدخل رمز الائتمان الاجتماعي الموحّد — <span class=\"vid\">91330683MA29E0KR3C</span> (المصنع) أو <span class=\"vid\">91330683MA2JQPJT6U</span> (شركة التصدير).",
        "تأكّد من تطابق اسم الشركة والممثل القانوني والعنوان المسجّل مع ما هو مذكور في هذه الصفحة.",
    ],
    s2t="شهادات يمكنك التحقّق منها",
    s2s="يمكن التحقّق من كل شهادة أدناه عبر الجهة المُصدِرة أو منصة حكومية. صور الشهادات معروضة في صفحة «من نحن».",
    t_head=["الشهادة", "الرقم", "الجهة المُصدِرة", "صالحة حتى", "مكان التحقّق"],
    t_rows=[
        ["ISO 9001:2015 — نظام إدارة الجودة", "<span class=\"vid\">04625Q15304R1M</span>",
         "Beijing Head International Certification Co., Ltd. (CNAS C046-M)", "2028-11-16",
         "منصة CNCA: <a href=\"https://cx.cnca.cn\" target=\"_blank\" rel=\"noopener\">cx.cnca.cn</a>"],
        ["CCC — شهادة الصين الإلزامية", "<span class=\"vid\">2024010702612682</span>",
         "China Quality Certification Centre (CQC)", "2029-03-11",
         "CQC: <a href=\"http://www.cqc.com.cn\" target=\"_blank\" rel=\"noopener\">www.cqc.com.cn</a> / منصة CNCA"],
        ["CE — توجيه EMC 2014/30/EU", "<span class=\"vid\">XH2601E0321945GC</span> (تقرير اختبار <span class=\"vid\">XH2601E0321945GR</span>)",
         "XHIT — Xhiua International Testing &amp; Certification (Shenzhen) Co., Ltd.", "—",
         "الجهة المُصدِرة: <a href=\"https://www.xhit-lab.com\" target=\"_blank\" rel=\"noopener\">www.xhit-lab.com</a>"],
        ["نظام CB — تقرير اختبار السلامة (IEC 60335-2-80)", "رقم التقرير <span class=\"vid\">60444427 001</span>",
         "TÜV Rheinland (LCIE)", "—", "التقرير متاح عند الطلب"],
    ],
    t_note="بالنسبة لنظام CB نملك حالياً تقرير اختبار TÜV Rheinland المعتمد؛ ويمكن ترتيب شهادة CB كاملة عند الطلب. تُرسَل تقارير الاختبار ونسخ الشهادات مع كل عرض سعر.",
    s3t="المستفيد البنكي وأمان الدفع",
    s3s="هذا هو الاسم الذي يجب أن يظهر في التحويل البنكي. أي اسم آخر ليس نحن.",
    bn_label="اسم المستفيد الرسمي للدفع",
    bn="SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.",
    bn_note="اسم البنك ورقم الحساب ورمز SWIFT مدوّنة فقط في الفاتورة الأولية / العقد. لا نرسلها أبداً من بريد إلكتروني مجاني، ولا نغيّرها دون مكالمة فيديو مباشرة.",
    rules=[
        "<strong>إذا وصلتك رسالة تقول إن بياناتنا البنكية تغيّرت — توقّف.</strong> لا تدفع، وتأكّد معنا أولاً بمكالمة فيديو أو رقم هاتف معروف.",
        "تأكّد أن اسم المستفيد في الفاتورة يطابق <strong>SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.</strong> تماماً — لا شركة أخرى ولا اسم شخصي.",
        "<strong>لا نطلب أبداً</strong> الدفع إلى حساب شخصي أو إلى شركة طرف ثالث.",
        "طابِق كل مستند مع الرموز وأرقام الشهادات المذكورة في هذه الصفحة.",
    ],
    s4t="تدقيق المصنع وجولة فيديو مباشرة",
    s4s="تفضّل أن ترى بنفسك؟ نوفّر جولات فيديو مباشرة في المصنع، ويمكننا مشاركة تقارير فحص من طرف ثالث وطاقة الإنتاج وسجلات التصدير لأغراض التحقّق.",
    cta_h="جاهز للتحقّق والطلب؟",
    cta_p="أرسل متطلباتك — واطلب الشهادات أو جولة فيديو أو تقرير تدقيق المصنع مع عرض السعر.",
    cta_a="/ar/contact/", cta_at="اطلب عرض سعر",
    cta_b="/baer-fan-catalog.pdf", cta_bt="تحميل الكتالوج PDF",
    updated="آخر تحديث: 9 أكتوبر 2026",
    footer_desc="مصنّع ومصدّر لمراوح الشفط · الشرق الأوسط وأوروبا وأمريكا الشمالية",
    footer_verify="تحقّق من شركتنا", footer_priv="سياسة الخصوصية", footer_cookie="ملفات تعريف الارتباط",
    bc_home="الرئيسية", bc_name="تحقّق من شركتنا",
)

C['zh'] = dict(
    lang='zh-CN', dir='ltr', robots="noindex,follow",
    title="核验 BAER 巴尔通风 | 主体资质·认证证书·收款户名",
    desc="在订货或付款前核验 BAER 巴尔通风（浙江巴尔电器科技有限公司）的主体资质、ISO 9001 / CCC / CE 认证证书编号与银行收款户名。",
    og_locale='zh_CN',
    nav=[("/zh/", "首页"), ("/zh/products/", "产品中心"), ("/zh/about/", "关于我们"), ("/resources", "资源中心"), ("/zh/contact/", "联系我们")],
    langbtn="中文", langlinks=[("https://baer-ventilation.com/verify/", "EN"), ("https://baer-ventilation.com/zh/verify/", "中文"), ("https://baer-ventilation.com/ar/verify/", "العربية")],
    h1="核验 BAER 巴尔通风",
    hero="下单与付款之前，先核验我们的主体资质、认证证书与银行收款户名。",
    crumbs=[("/zh/", "首页"), (None, "公司资质核验")],
    s1t="你在和谁做生意",
    s1s="BAER 巴尔通风是一个工厂集团：合同与收款由我们全资持有的出口公司承接。以下是两个法律主体，均可在中国官方系统查询。",
    e1_role="生产主体（工厂）",
    e1_name="浙江巴尔电器科技有限公司",
    e1_rows=[("统一社会信用代码", "91330683MA29E0KR3C"),
             ("法定代表人", "吕锋平"),
             ("注册地址", "浙江省绍兴市嵊州市甘霖镇经五路 8-1 号（邮编 312400）"),
             ("成立时间", "2017 年（工厂可追溯至 2003 年）"),
             ("承担职能", "生产制造、质量控制、注塑、电机绕线、产品认证")],
    e2_role="出口与收款主体",
    e2_name="绍兴巴尔进出口有限公司",
    e2_rows=[("统一社会信用代码", "91330683MA2JQPJT6U"),
             ("法定代表人", "吕锋平（同一人）"),
             ("注册地址", "浙江省绍兴市嵊州市三江街道领带园二路 3 号智创小微企业园 3 号楼 6 层"),
             ("成立时间", "2020 年"),
             ("海关备案", "2020-12-04 于绍兴海关备案为进出口货物收发货人（有效期至 2068 年）"),
             ("承担职能", "签订合同、开具形式发票、出口单证与收款")],
    rel_note="<strong>两者关系：</strong>绍兴巴尔进出口有限公司由浙江巴尔电器科技有限公司 100% 全资持股，法定代表人同为一人。这是中国制造企业的通行结构——工厂负责生产，自营进出口公司负责签约与收款。",
    gsxt_title="如何在官方系统核验我们",
    gsxt_steps=[
        "打开<strong>国家企业信用信息公示系统（gsxt）</strong>：<a href=\"https://www.gsxt.gov.cn\" target=\"_blank\" rel=\"noopener\">https://www.gsxt.gov.cn</a>",
        "输入统一社会信用代码——<span class=\"vid\">91330683MA29E0KR3C</span>（工厂）或 <span class=\"vid\">91330683MA2JQPJT6U</span>（出口公司）。",
        "核对公司名称、法定代表人与注册地址是否与本页一致。",
    ],
    s2t="可查证的认证证书",
    s2s="以下每一张证书都可向发证机构或政府平台核对。证书图片见「关于我们」页。",
    t_head=["证书", "编号", "发证机构", "有效期至", "查询入口"],
    t_rows=[
        ["ISO 9001:2015 质量管理体系", "<span class=\"vid\">04625Q15304R1M</span>",
         "Beijing Head International Certification Co., Ltd.（CNAS C046-M）", "2028-11-16",
         "CNCA 全国认证认可信息公共服务平台：<a href=\"https://cx.cnca.cn\" target=\"_blank\" rel=\"noopener\">cx.cnca.cn</a>"],
        ["CCC 中国国家强制性产品认证", "<span class=\"vid\">2024010702612682</span>",
         "中国质量认证中心（CQC）", "2029-03-11",
         "CQC 官网：<a href=\"http://www.cqc.com.cn\" target=\"_blank\" rel=\"noopener\">www.cqc.com.cn</a> / CNCA 平台"],
        ["CE — EMC 指令 2014/30/EU", "<span class=\"vid\">XH2601E0321945GC</span>（测试报告 <span class=\"vid\">XH2601E0321945GR</span>）",
         "深圳华检 XHIT — Xhiua International Testing &amp; Certification (Shenzhen) Co., Ltd.", "—",
         "发证机构官网：<a href=\"https://www.xhit-lab.com\" target=\"_blank\" rel=\"noopener\">www.xhit-lab.com</a>"],
        ["CB 体系 — 安全测试报告（IEC 60335-2-80）", "报告编号 <span class=\"vid\">60444427 001</span>",
         "TÜV Rheinland（LCIE 出具）", "—", "报告可按需提供"],
    ],
    t_note="CB 体系目前持有 TÜV Rheinland 认可测试报告；完整 CB 证书可按需办理。每次报价均随附测试报告与证书扫描件。",
    s3t="收款户名与付款安全",
    s3s="以下是你电汇时收款人一栏必须出现的名称——除此以外的名称都不是我们。",
    bn_label="官方收款户名",
    bn="SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.",
    bn_note="开户行、账号与 SWIFT 码只出现在你的形式发票／合同中。我们绝不会用免费邮箱发送这些信息，也绝不会在未视频确认的情况下变更账号。",
    rules=[
        "<strong>若收到任何「银行账号已变更」的邮件——立即停手，不要付款。</strong>请先通过视频通话或已知电话与我们核实。",
        "核对形式发票上的收款人名称是否与 <strong>SHAOXING BAER IMPORT &amp; EXPORT CO., LTD.</strong> 完全一致，不得出现其他公司或个人名字。",
        "<strong>我们绝不会</strong>要求把货款打入个人账户或第三方公司账户。",
        "所有单据请与本页列出的信用代码、证书编号逐项比对。",
    ],
    s4t="验厂与实时视频看厂",
    s4s="想亲自看看？我们提供实时视频看厂，也可按需提供第三方验厂报告、产能数据与出口记录，供你尽职调查。",
    cta_h="准备好核验并下单了吗？",
    cta_p="把你的需求发给我们——可在索取报价的同时，一并索要证书、视频看厂或验厂报告。",
    cta_a="/zh/contact/", cta_at="索取报价",
    cta_b="/baer-fan-catalog.pdf", cta_bt="下载产品目录 PDF",
    updated="最后更新：2026 年 10 月 9 日",
    footer_desc="换气扇制造商与出口商 · 中东、欧洲、北美",
    footer_verify="公司资质核验", footer_priv="隐私政策 Privacy Policy", footer_cookie="Cookie 声明",
    bc_home="首页", bc_name="公司资质核验",
)


def head_html(c, lang):
    # hreflang：zh 为 noindex，不给 alternate（与 zh/about 一致）
    alts = ""
    if lang == 'en':
        alts = ('<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/verify/">\n'
                '<link rel="alternate" hreflang="ar" href="https://baer-ventilation.com/ar/verify/">\n'
                '<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/verify/">')
    elif lang == 'ar':
        alts = ('<link rel="alternate" hreflang="ar" href="https://baer-ventilation.com/ar/verify/">\n'
                '<link rel="alternate" hreflang="en" href="https://baer-ventilation.com/verify/">\n'
                '<link rel="alternate" hreflang="x-default" href="https://baer-ventilation.com/verify/">')
    canonical = {"en": "https://baer-ventilation.com/verify/",
                 "ar": "https://baer-ventilation.com/ar/verify/",
                 "zh": "https://baer-ventilation.com/zh/verify/"}[lang]
    robots = '<meta name="robots" content="%s">\n' % c['robots'] if c['robots'] else ''
    img = "https://baer-ventilation.com/assets/images/A4fa2bde5c7754b548a9cf5da5e3bec3aQ.webp"

    # JSON-LD block A
    blockA = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": c['title'],
        "url": canonical,
        "mainEntity": dict(ORG),
    }
    # JSON-LD block B
    inl = {"en": "en", "ar": "ar", "zh": "zh-CN"}[lang]
    blockB = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": canonical, "url": canonical, "name": c['bc_name'],
             "isPartOf": {"@id": "https://baer-ventilation.com/#website"},
             "inLanguage": inl, "description": c['desc'],
             "breadcrumb": {"@id": canonical + "#breadcrumb"}},
            {"@type": "BreadcrumbList", "@id": canonical + "#breadcrumb",
             "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": c['bc_home'],
                  "item": {"en": "https://baer-ventilation.com/", "ar": "https://baer-ventilation.com/ar/",
                           "zh": "https://baer-ventilation.com/zh/"}[lang]},
                 {"@type": "ListItem", "position": 2, "name": c['bc_name'], "item": canonical},
             ]},
        ],
    }

    return ('<!DOCTYPE html>\n<html lang="%s" dir="%s">\n<head>\n'
            '<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '%s\n%s'
            '<title>%s</title>\n'
            '<meta name="description" content="%s">\n'
            '<link rel="canonical" href="%s">\n%s\n'
            '<meta property="og:type" content="website">\n'
            '<meta property="og:site_name" content="BAER Ventilation">\n'
            '<meta property="og:locale" content="%s">\n'
            '<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="%s">\n'
            '<meta property="og:image:alt" content="%s">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="twitter:title" content="%s">\n'
            '<meta name="twitter:description" content="%s">\n'
            '<meta name="twitter:image" content="%s">\n'
            '<meta name="theme-color" content="#0F172A">\n'
            '<link rel="stylesheet" href="/css/style.css">\n'
            '<link rel="stylesheet" href="/css/main.css">\n'
            '<style>\n%s\n</style>\n'
            '<script type="application/ld+json">\n%s\n</script>\n'
            '<style>\n%s\n</style>\n'
            '<script type="application/ld+json">\n%s\n</script>\n'
            '</head>\n'
            ) % (
        c['lang'], c['dir'], GTM, robots,
        c['title'], c['desc'], canonical, alts,
        c['og_locale'], c['title'], c['desc'], canonical, img, c['title'],
        c['title'], c['desc'], img,
        CSS_COMMON,
        json.dumps(blockA, ensure_ascii=False, indent=2),
        BC_CSS,
        json.dumps(blockB, ensure_ascii=False, indent=2),
    )


def nav_html(c):
    items = "\n".join('<a href="%s">%s</a>' % (h, t) for h, t in c['nav'])
    langs = "\n".join('<a href="%s">%s</a>' % (h, t) for h, t in c['langlinks'])
    return ('<body>\n'
            '<nav class="navbar">\n'
            '  <div class="container nav-content">\n'
            '    <a href="/" class="logo">BAER<span>.</span></a>\n'
            '    <div class="nav-links">\n'
            '      %s\n'
            '      <div class="lang-dropdown">\n'
            '        <div class="lang-btn">%s ▾</div>\n'
            '        <div class="lang-content">\n'
            '%s\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n'
            '  </div>\n'
            '</nav>\n') % (items, c['langbtn'], langs)


def entity(role, name, rows):
    dl = "\n".join('<dt>%s</dt>\n<dd>%s</dd>' % (k, v) for k, v in rows)
    return ('<div class="entity">\n<span class="role">%s</span>\n<h3>%s</h3>\n'
            '<dl>\n%s\n</dl>\n</div>') % (role, name, dl)


def table(head, rows):
    th = "".join('<th>%s</th>' % h for h in head)
    trs = ""
    for r in rows:
        trs += "<tr>" + "".join('<td>%s</td>' % x for x in r) + "</tr>\n"
    return '<table class="vtable">\n<thead><tr>%s</tr></thead>\n<tbody>\n%s</tbody>\n</table>' % (th, trs)


def body_html(c):
    crumb = ('<nav class="baer-breadcrumb" aria-label="Breadcrumb"><ol>'
             '<li><a href="%s">%s</a></li><li class="sep" aria-hidden="true">/</li>'
             '<li aria-current="page">%s</li></ol></nav>') % (c['crumbs'][0][0], c['crumbs'][0][1], c['crumbs'][1][1])
    steps = "\n".join('<li>%s</li>' % s for s in c['gsxt_steps'])
    rules = "\n".join('<li>%s</li>' % s for s in c['rules'])
    return (
        '<section class="page-hero">\n  <div class="container">\n    %s\n    <h1>%s</h1>\n    <p>%s</p>\n  </div>\n</section>\n\n'
        '<section class="section">\n  <div class="container">\n'
        '    <h2 class="sec-title">%s</h2>\n    <p class="sec-sub">%s</p>\n'
        '    <div class="grid-2">\n%s\n%s\n    </div>\n'
        '    <div class="note">%s</div>\n'
        '    <h3 style="text-align:center;margin:40px 0 6px;font-size:20px;font-weight:800;color:#0F172A;">%s</h3>\n'
        '    <ul class="steps">\n%s\n    </ul>\n'
        '  </div>\n</section>\n\n'
        '<section class="section alt">\n  <div class="container">\n'
        '    <h2 class="sec-title">%s</h2>\n    <p class="sec-sub">%s</p>\n'
        '    %s\n'
        '    <div class="note">%s</div>\n'
        '  </div>\n</section>\n\n'
        '<section class="section">\n  <div class="container">\n'
        '    <h2 class="sec-title">%s</h2>\n    <p class="sec-sub">%s</p>\n'
        '    <div class="alert">\n      <div class="lbl">%s</div>\n      <div class="bn">%s</div>\n      <p>%s</p>\n    </div>\n'
        '    <ul class="rules">\n%s\n    </ul>\n'
        '  </div>\n</section>\n\n'
        '<section class="section alt">\n  <div class="container">\n'
        '    <h2 class="sec-title">%s</h2>\n    <p class="sec-sub">%s</p>\n'
        '  </div>\n</section>\n\n'
        '<section class="cta-band">\n  <div class="container">\n'
        '    <h2>%s</h2>\n    <p>%s</p>\n'
        '    <div class="cta-actions">\n'
        '      <a href="%s" class="baer-btn-v2">%s</a>\n'
        '      <a href="%s" target="_blank" class="btn-ghost">%s</a>\n'
        '    </div>\n    <p class="updated" style="color:#94A3B8;">%s</p>\n'
        '  </div>\n</section>\n\n'
    ) % (
        crumb, c['h1'], c['hero'],
        c['s1t'], c['s1s'],
        entity(c['e1_role'], c['e1_name'], c['e1_rows']),
        entity(c['e2_role'], c['e2_name'], c['e2_rows']),
        c['rel_note'],
        c['gsxt_title'], steps,
        c['s2t'], c['s2s'], table(c['t_head'], c['t_rows']), c['t_note'],
        c['s3t'], c['s3s'], c['bn_label'], c['bn'], c['bn_note'], rules,
        c['s4t'], c['s4s'],
        c['cta_h'], c['cta_p'], c['cta_a'], c['cta_at'], c['cta_b'], c['cta_bt'], c['updated'],
    )


def footer_html(c):
    return (
        '<footer style="background:#0F172A;color:#94A3B8;padding:44px 0 30px;text-align:center;">\n'
        '  <div class="container">\n'
        '    <div style="font-size:20px;font-weight:900;color:#fff;margin-bottom:10px;">BAER<span style="color:#E21E26;">.</span> Ventilation</div>\n'
        '    <p style="font-size:13px;margin-bottom:16px;">%s</p>\n'
        '    <p style="font-size:13px;margin-bottom:16px;"><a href="https://www.youtube.com/@BAERVentilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">▶ YouTube: @BAERVentilation</a> · <a href="https://www.linkedin.com/company/baer-ventilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">LinkedIn</a></p>\n'
        '    <p style="font-size:12px;">&copy; 2026 BAER Ventilation. All rights reserved.</p>\n'
        '  </div>\n'
        '  <p style="margin:14px 0 0;font-size:12px;opacity:.85;">'
        '<a href="%s" style="color:inherit;text-decoration:underline;">%s</a> &middot; '
        '<a href="/privacy/" style="color:inherit;text-decoration:underline;">%s</a> &middot; '
        '<a href="/privacy/#cookies" style="color:inherit;text-decoration:underline;">%s</a></p>\n'
        '</footer>\n'
        '<script>\n'
        "document.addEventListener('click', function(e){\n"
        "  var t = e.target;\n"
        "  while (t && t !== document.body && t.tagName !== 'A') { t = t.parentElement; }\n"
        "  if (!t || t.tagName !== 'A' || typeof gtag !== 'function') return;\n"
        "  var href = t.getAttribute('href') || '';\n"
        "  if (/wa\\.me|whatsapp/i.test(href)) { gtag('event', 'whatsapp_click'); }\n"
        "  else if (href.indexOf('mailto:') === 0) { gtag('event', 'email_click'); }\n"
        "  else if (/\\.pdf(\\?|$)/i.test(href)) { gtag('event', 'catalog_download'); }\n"
        "  else if (href.indexOf('tel:') === 0) { gtag('event', 'phone_click'); }\n"
        "});\n"
        "</script>\n"
        '<script src="/js/main.js"></script>\n'
        '<script src="/js/reveal.js?v=1" defer></script>\n'
        '</body>\n</html>\n'
    ) % (c['footer_desc'], self_verify_href(c), c['footer_verify'], c['footer_priv'], c['footer_cookie'])


def self_verify_href(c):
    return {"en": "/verify/", "ar": "/ar/verify/", "zh": "/zh/verify/"}[
        'en' if c['lang'] == 'en' else ('ar' if c['lang'] == 'ar' else 'zh')]


TARGETS = {
    'en': os.path.join(ROOT, 'verify', 'index.html'),
    'ar': os.path.join(ROOT, 'ar', 'verify', 'index.html'),
    'zh': os.path.join(ROOT, 'zh', 'verify', 'index.html'),
}


def build(lang):
    c = C[lang]
    html = head_html(c, lang) + nav_html(c) + body_html(c) + footer_html(c)
    return html


def main():
    apply = '--apply' in sys.argv
    for lang in ('en', 'ar', 'zh'):
        html = build(lang)
        p = TARGETS[lang]
        # 自检：JSON-LD 可解析 + 关键元素存在
        import re
        blocks = re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', html, re.S)
        for b in blocks:
            json.loads(b)
        assert html.count('<footer') == 1 and html.count('</html>') == 1
        assert html.count('<nav class="navbar">') == 1
        org = sum(b.count('"Organization"') for b in blocks)
        print(f"[{lang}] {p}  bytes={len(html.encode('utf-8'))}  jsonld_blocks={len(blocks)}  Organization_refs={org}")
        if apply:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            io.open(p, 'w', encoding='utf-8', newline='\n').write(html)
    print("APPLIED" if apply else "DRY-RUN (加 --apply 写入)")


if __name__ == '__main__':
    main()
