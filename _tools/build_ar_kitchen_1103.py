# -*- coding: utf-8 -*-
"""Build /ar/commercial-kitchen-exhaust-fans.html (Arabic RTL version of the kitchen page).

Source of truth for CSS / structure: commercial-kitchen-exhaust-fans.html
RTL conventions: match existing ar/*.html (inset-inline-end, Noto Sans Arabic, text-align:start)
"""
import re, os

ROOT = r"D:/WorkBuddy/2026-10-08-15-46-08/site"
EN = os.path.join(ROOT, "commercial-kitchen-exhaust-fans.html")
OUT = os.path.join(ROOT, "ar", "commercial-kitchen-exhaust-fans.html")
BASE = "https://baer-ventilation.com"
URL_AR = BASE + "/ar/commercial-kitchen-exhaust-fans"
URL_EN = BASE + "/commercial-kitchen-exhaust-fans"

src = open(EN, encoding="utf-8").read()

# ---------- reuse the two style blocks verbatim ----------
styles = re.findall(r"<style>.*?</style>", src, re.S)
assert len(styles) >= 2, len(styles)
MAIN_CSS = styles[0]
TOP_CSS = styles[1]

RTL_CSS = """<style>/* rtl adjustments */
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Noto Sans Arabic',Tahoma,Arial,sans-serif;}
.hero h1{letter-spacing:0;line-height:1.35;}
.hero-cat,.section-tag{letter-spacing:.6px;}
.spec-table th,.spec-table td,.ptable th,.ptable td{text-align:right;}
.floating{right:auto;inset-inline-end:18px;}
.hero-cta{justify-content:flex-start;}
.ctabox .hero-cta{justify-content:center;}
.tnote{text-align:right;}
</style>"""

CLARITY = """<!-- Microsoft Clarity -->
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "y7asoc678j");
</script>"""

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0Y7GNF2D0H"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0Y7GNF2D0H');
</script>"""

TITLE = "مراوح عادم المطابخ التجارية &mdash; سلسلة BXF الأنبوبية | باير"
DESC = ("مراوح عادم مطابخ بأنابيب مختلطة التدفق، 290&ndash;2,200 m&sup3;/h وحتى 693 Pa، لخطوط طرد "
        "المقاهي والمطاعم وغسيل الأطباق وهواء التعويض. جداول تحجيم حسب نوع المطبخ.")
OG_DESC = ("مراوح قنوات مختلطة التدفق من 290 إلى 2,200 m3/h وحتى 693 Pa. تحجيم حسب طول الهود "
           "ومرات تبديل الهواء وهواء التعويض. توريد مباشر من المصنع، معتمدة CE.")
IMG = BASE + "/assets/images/Hf77c8f2216ff4576b9f83c896fdd000fq.webp"

HEAD = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL_AR}">
<link rel="alternate" hreflang="ar" href="{URL_AR}">
<link rel="alternate" hreflang="en" href="{URL_EN}">
<link rel="alternate" hreflang="x-default" href="{URL_EN}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BAER Ventilation">
<meta property="og:locale" content="ar_SA">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{OG_DESC}">
<meta property="og:url" content="{URL_AR}">
<meta property="og:image" content="{IMG}">
<meta property="og:image:alt" content="مروحة قناة مختلطة التدفق BXF لطرد مطابخ المطاعم | BAER Ventilation">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="مراوح قنوات 100-315 مم لطرد المطابخ وهواء التعويض. جداول تحجيم حسب نوع المطبخ وسرعة القناة وميزانية الضغط.">
<meta name="twitter:image" content="{IMG}">
<meta name="theme-color" content="#0F172A">
{CLARITY}
{GTAG}
{MAIN_CSS}
{TOP_CSS}
{RTL_CSS}
</head>"""

TOPBAR = """<body>

<div class="bv-topbar">
        <div class="bv-topbar-in">
            <a class="bv-mail" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
            <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">
                <span class="bv-tel">WhatsApp/WeChat: +86 136 5585 9122</span>
                <a class="bv-wa-btn" href="https://wa.me/8613655859122?text=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7%20BAER%D8%8C%20%D8%A3%D8%B1%D8%BA%D8%A8%20%D9%81%D9%8A%20%D9%85%D8%B9%D8%B1%D9%81%D8%A9%20%D8%A7%D9%84%D9%85%D8%B2%D9%8A%D8%AF%20%D8%B9%D9%86%20%D9%85%D8%B1%D8%A7%D9%88%D8%AD%20%D8%A7%D9%84%D8%AA%D9%87%D9%88%D9%8A%D8%A9." target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.5A9.9 9.9 0 1 0 12.04 2Zm5.8 14.2c-.25.7-1.45 1.35-2 1.4-.55.05-1.05.25-3.5-.75-2.95-1.2-4.8-4.25-4.95-4.45-.15-.2-1.15-1.55-1.15-2.95 0-1.4.75-2.1 1-2.4.25-.3.55-.35.75-.35h.55c.2 0 .4-.05.65.5.25.6.85 2 .9 2.15.05.15.1.3 0 .5-.1.2-.15.35-.3.55-.15.2-.3.45-.45.6-.15.15-.3.35-.15.65.15.3.75 1.25 1.6 2 1.1 1 2 1.3 2.3 1.45.3.15.5.1.65-.05.2-.2.7-.8.9-1.05.2-.3.4-.25.65-.15.25.1 1.65.8 1.95.95.3.15.5.2.55.35.05.1.05.7-.2 1.4Z"/></svg><span>WhatsApp</span></a>
            </div>
        </div>
    </div>

    <nav class="navbar">
  <div class="nav-inner">
    <a href="https://baer-ventilation.com/ar/" class="logo">BAER<span>VENT</span></a>
    <div class="nav-links">
      <a href="https://baer-ventilation.com/ar/">الرئيسية</a>
      <a href="https://baer-ventilation.com/ar/products/">المنتجات</a>
      <a href="https://baer-ventilation.com/ar/about/">من نحن</a>
      <a href="https://baer-ventilation.com/ar/contact/">اتصل بنا</a>
      <a href="https://baer-ventilation.com/baer-fan-catalog.pdf" target="_blank">الكتالوج</a>
    </div>
    <div class="lang-switch">
      <a href="https://baer-ventilation.com/commercial-kitchen-exhaust-fans">EN</a>
      <a href="https://baer-ventilation.com/ar/commercial-kitchen-exhaust-fans" class="active">العربية</a>
    </div>
  </div>
</nav>

<section class="hero">
  <div class="hero-inner">
    <span class="hero-cat">تهوية المطابخ التجارية</span>
    <h1>مراوح عادم المطابخ التجارية: أنظمة قنوات مختلطة التدفق</h1>
    <p>طرد الهواء في المطبخ يفشل لسببين: إما أن المروحة لا تستطيع مقاومة الضغط على طول مسار القناة، أو أن أحداً لم يحسب هواء التعويض. مراوح <strong>BXF</strong> مختلطة التدفق تغطي <strong>290&ndash;2,200 m&sup3;/h</strong> وحتى <strong>693 Pa</strong> بستة مقاسات من 100 إلى 315 مم، لمقاهي ومطاعم وكافيتريات ومطابخ غسيل الأطباق، حيث تُركَّب المروحة في نهاية المسار لا داخل الجدار.</p>
    <p style="font-size:13px;color:#64748B;margin:10px 0 0;">آخر تحديث: 3 نوفمبر 2026</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        استفسار واتساب
      </a>
      <a class="btn btn-red" href="https://baer-ventilation.com/ar/contact/">اطلب عرض سعر</a>
      <a class="btn btn-ghost" href="https://baer-ventilation.com/cfm-calculator">حاسبة تدفق الهواء</a>
    </div>
  </div>
</section>

<div class="crumb">
  <a href="https://baer-ventilation.com/ar/">الرئيسية</a> / <a href="https://baer-ventilation.com/ar/products/">المنتجات</a> / <span>مراوح عادم المطابخ التجارية</span>
</div>

<div class="container">

  <p style="font-size:16.5px;line-height:1.9;max-width:900px;margin-bottom:44px;">المطبخ التجاري أصعب مهمة تهوية في المبنى: حرارة ودهون ورطوبة، ومسار قناة ضُبط بعد أن صُمِّم المبنى. تشرح هذه الصفحة ما تستطيعه مروحة القناة مختلطة التدفق في المطبخ وما لا تستطيعه، وكيف تُحجَّم كمية الطرد وهواء التعويض الذي يجب أن يحلّ محلها، وأي طراز <strong>BXF</strong> يناسب كل مساحة &mdash; حتى تصل المروحة التي تطلبها بتدفقها المعلن فعلاً بعد أن يعترضه الفلتر والأكواع وشبك الجدار.</p>
"""

BODY1 = """
  <h2 class="sec">السؤال الأول: هل الهواء مشبع بالدهون؟</h2>
  <div class="appgrid">
      <div class="appcard"><h4>طهي خفيف مع فلتر حاجزي &mdash; BXF هو الخيار</h4><p>أفران كهربائية وصواني تسخين ومايكروويف ومحطات قهوة وشاي وخطوط حفظ ساخن. حمل الدهون منخفض، ويُركَّب فلتر حاجزي من الستيل في الهود، ثم تأتي مروحة القناة بعده عند نهاية الطرد. هذه هي الحالة التي كُتبت لها هذه الصفحة.</p></div>
      <div class="appcard"><h4>قلايات عميقة وقدور ووك وشوّابات &mdash; راجع حمل الدهون</h4><p>القلي الثقيل يضخ دهوناً أكثر بكثير في القناة. في الشرق الأوسط وجنوب شرق آسيا تُستخدم مروحة القناة في هذا التطبيق على نطاق واسع، وهي تعمل عندما تتحقق ثلاثة أمور: فلتر حاجزي من الستيل على الهود، والمروحة عند نهاية الطرد لا فوق خط الطهي، ودفاعة تُغسل كل موسم (<a href="https://baer-ventilation.com/exhaust-fan-maintenance-guide" style="color:#C0392B;font-weight:600;">جدول الصيانة</a> يحدد الفترة حسب حمل الدهون). وحيث يفرض المشروع كود حماية من الحريق يسمّي مروحة معتمدة للدهون، فالكود هو المرجع &mdash; أرسل لنا البند وسنقول ما يحتاجه التركيب.</p></div>
  </div>
  <p style="max-width:900px;margin-top:22px;">في الممارسة، الفرق في الصيانة لا في المروحة. الدهون المتراكمة على الدفاعة تُفقدها توازنها، والدفاعة غير المتوازنة هي ما يتعطل &mdash; لا حجم المحرك. أعطِ الخط فلتراً وفتحة تنظيف ومروحة يمكن الوصول إليها دون فك القناة، وسعمل مروحة قناة في مطبخ مطعم صغير سنوات. تدفق الهواء والضغط وسرعة القناة تُحسب بالطريقة نفسها في الحالتين، لذا أرقام الهود أدناه تنطبق في كل حالة.</p>

  <span class="section-tag">مطابقة الطراز</span>
  <h2 class="sec">أي طراز لأي مساحة في المطبخ</h2>
  <div class="appgrid">
      <div class="appcard"><h4>كافيتريا الموظفين / غرفة الشاي</h4><p>تسخين فقط دون قلي. 8&ndash;10 مرات تبديل هواء: <strong>BXF-150</strong> (620 m&sup3;/h) حتى 70 m&sup3;، ووحدتان فوق ذلك.</p></div>
      <div class="appcard"><h4>مقهى وطهي خفيف وهود حتى 1.5 م</h4><p>1,200&ndash;2,200 m&sup3;/h عند 200&ndash;300 Pa: <strong>BXF-315</strong> واحدة، أو <strong>BXF-200</strong> اثنتان على التوازي إذا كان في المسار عدة أكواع.</p></div>
      <div class="appcard"><h4>مسار هود مطعم من 1.5 إلى 3 م</h4><p>3,000&ndash;4,500 m&sup3;/h عند 250&ndash;400 Pa: <strong>وحدتان BXF-315 على التوازي</strong> في غرفة تجميع مشتركة. وحدة واحدة لا تحمل هذا الحمل.</p></div>
      <div class="appcard"><h4>غسيل الأطباق والقدور</h4><p>بخار ورطوبة، 15&ndash;20 مرة تبديل هواء: <strong>BXF-200</strong> أو <strong>BXF-250</strong>، مع ميل القناة راجعاً إلى مصرف حتى لا تتجمع المياه المتكثفة داخل المروحة.</p></div>
      <div class="appcard"><h4>غرفة التحضير / المخزن الجاف</h4><p>إزالة الحرارة والروائح، 10&ndash;12 مرة تبديل هواء: <strong>BXF-150</strong> أو <strong>BXF-200</strong>، مركّبة في الطرف المقابل للباب.</p></div>
      <div class="appcard"><h4>هواء التعويض (جانب الإمداد)</h4><p>85% من حجم الطرد، يُدخَل بعيداً عن واجهة الهود: <strong>BXF-250</strong> أو <strong>BXF-315</strong>، مع صندوق فلتر على السحب.</p></div>
  </div>

  <span class="section-tag">التحجيم</span>
  <h2 class="sec">تحجيم طرد المطبخ بثلاثة أرقام</h2>
  <p style="max-width:900px;"><strong>1. طول الهود.</strong> احسب 100 CFM لكل قدم طولي من واجهة الهود للحمل الخفيف، و200 للمتوسط (شوّابات وقلايات تحت فلتر)، و300 للثقيل. هذا يعادل نحو 0.5 م/ث سرعة على الواجهة، وهو الرقم الذي تنشره معظم شركات الهودات.</p>
  <p style="max-width:900px;"><strong>2. التحويل وإضافة الهامش.</strong> 1 CFM = 1.7 m&sup3;/h. أضف 20% للفلتر الحاجزي والأكواع وشبك الجدار &mdash; المروحة المعلنة عند 2,200 m&sup3;/h هواء حر لا تعطي 2,200 عبر فلتر دهني وثلاثة أكواع.</p>
  <p style="max-width:900px;"><strong>3. عوّض 85% منه.</strong> هواء التعويض ليس اختيارياً: مع إغلاق المطبخ تختنق مروحة الطرد، وينخفض التدفق بمقدار الثلث أو أكثر، ويفقد الهود قدرته على احتجاز الدهون والبخار، وتصبح الأبواب صعبة الفتح، ويمكن أن ترتد أجهزة الغاز إلى الداخل.</p>

  <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:26px;margin:26px 0 44px;max-width:900px;">
    <h4 style="margin:0 0 10px;font-size:16px;">مثال محسوب &mdash; هود 2.4 م (8 قدم) بحمل متوسط</h4>
    <p style="margin:0;">8 قدم &times; 200 CFM = <strong>1,600 CFM = 2,715 m&sup3;/h</strong>. ومع هامش 20%: <strong>3,260 m&sup3;/h</strong> عند نحو 250&ndash;350 Pa. وحدتان <strong>BXF-250</strong> على التوازي تعطيان 3,600 m&sup3;/h عند 488 Pa &mdash; أصغر تجميع يحقق الحمل. هواء التعويض بنسبة 85%: <strong>2,770 m&sup3;/h</strong>، أي <strong>BXF-315</strong> و<strong>BXF-150</strong>، يُدخَلان من مستوى منخفض في الجانب المقابل للهود.</p>
  </div>

  <span class="section-tag">سرعة القناة</span>
  <h2 class="sec">سرعة الهواء في القناة: الرقم الذي يفحصه المقاولون</h2>
  <p style="max-width:900px;">السرعة هي التدفق مقسوماً على مساحة مقطع القناة، وهي التي تحدد الضجيج وفقد الضغط وهل تبقى الدهون متحركة. لقناة دهون، 7.6&ndash;10 م/ث (1,500&ndash;2,000 fpm) تمنع استقرار الرواسب. وللطرد العام، 5&ndash;8 م/ث مريحة. عند التدفق المعلن:</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>الطراز</th><th>مقاس القناة (mm)</th><th>التدفق المعلن (m&sup3;/h)</th><th>سرعة القناة (م/ث)</th><th>ملاحظة</th></tr>
  <tr><td><strong>BXF-100</strong></td><td>&Phi;100</td><td>290</td><td>10.3</td><td>مسارات قصيرة فقط &mdash; مسموعة عند هذه السرعة</td></tr>
  <tr><td><strong>BXF-125</strong></td><td>&Phi;125</td><td>420</td><td>9.5</td><td>داخل نطاق قناة الدهون</td></tr>
  <tr><td><strong>BXF-150</strong></td><td>&Phi;150</td><td>620</td><td>9.8</td><td>طرد الكافيتريا وغرفة التحضير</td></tr>
  <tr><td><strong>BXF-200</strong></td><td>&Phi;200</td><td>1,200</td><td>10.6</td><td>كبّر القناة درجة واحدة في المسارات الطويلة</td></tr>
  <tr><td><strong>BXF-250</strong></td><td>&Phi;250</td><td>1,800</td><td>10.2</td><td>أفضل ضغط بين المقاسات الصغيرة</td></tr>
  <tr><td><strong>BXF-315</strong></td><td>&Phi;315</td><td>2,200</td><td>7.8</td><td>النقطة المثالية لمسارات قنوات المطابخ</td></tr>
  </table>
  </div>
  <p class="tnote">السرعة محسوبة عند التدفق الحر المعلن عبر قناة بقطر المروحة نفسه. كل زيادة 100 مم في مقاس القناة تخفض السرعة نحو 40% وتنتزع 10&ndash;20 dB(A) من الضجيج &mdash; وإذا وجب أن يكون المسار هادئاً، استخدم قناة أكبر ومخفّضاً عند المروحة.</p>
"""

BODY2 = """
  <span class="section-tag">الضغط</span>
  <h2 class="sec">ميزانية الضغط: ما يجب أن تتغلب عليه المروحة فعلاً</h2>
  <p style="max-width:900px;">أرقام الكتالوج هي هواء حر عند 0 Pa. والمطبخ لا يكون هواء حراً أبداً. اجمع المقاومات قبل اختيار الطراز:</p>
  <div class="twrap">
  <table class="spec-table">
  <tr><th>المكوّن</th><th>فقد الضغط النموذجي</th></tr>
  <tr><td>فلتر دهون حاجزي من الستيل</td><td>50&ndash;100 Pa (يزيد مع التحميل)</td></tr>
  <tr><td>شبك الجدار / مظلة خارجية</td><td>30&ndash;50 Pa</td></tr>
  <tr><td>كل كوع 90&deg;</td><td>15&ndash;25 Pa</td></tr>
  <tr><td>قناة مستقيمة، لكل متر</td><td>3&ndash;5 Pa</td></tr>
  <tr><td>وصلة مرنة، لكل واحدة</td><td>10 Pa</td></tr>
  </table>
  </div>
  <p class="tnote">مثال: 6 م قناة (30 Pa) + 3 أكواع (60 Pa) + فلتر (80 Pa) + شبك (40 Pa) = <strong>210 Pa</strong> فوق ما يحتاجه الهود نفسه. اختر الطراز الذي يعطي منحنى أدائه تدفقك عند ذلك الضغط &mdash; في سلسلة BXF يعني ذلك عادةً BXF-200 وما فوق. أرسل رسم المسار ونختار لك الطراز.</p>

  <span class="section-tag">مجموعة الطرازات</span>
  <h2 class="sec">طرازات BXF الستة</h2>
  <div class="twrap">
  <table class="spec-table">
  <tr><th rowspan="2">الطراز</th><th>القناة</th><th>التدفق</th><th>التدفق</th><th>أقصى ضغط ساكن</th><th>القدرة</th><th>الضوضاء</th><th>عدد/كرتون</th><th>الحجم</th><th>الوزن الإجمالي</th></tr>
  <tr><th class="unit">(mm)</th><th class="unit">(m&sup3;/h)</th><th class="unit">(CFM)</th><th class="unit">(Pa)</th><th class="unit">(W)</th><th class="unit">(dB A)</th><th class="unit">(قطعة)</th><th class="unit">(m&sup3;)</th><th class="unit">(kg/كرتون)</th></tr>
  <tr><td><strong>BXF-100</strong></td><td>&Phi;100</td><td>290</td><td>171</td><td>150</td><td>48</td><td>28&ndash;31</td><td>6</td><td>0.101</td><td>11.20</td></tr>
  <tr><td><strong>BXF-125</strong></td><td>&Phi;125</td><td>420</td><td>247</td><td>180</td><td>50</td><td>28&ndash;31</td><td>6</td><td>0.101</td><td>12.70</td></tr>
  <tr><td><strong>BXF-150</strong></td><td>&Phi;150</td><td>620</td><td>365</td><td>300</td><td>60</td><td>28&ndash;32</td><td>6</td><td>0.119</td><td>15.45</td></tr>
  <tr><td><strong>BXF-200</strong></td><td>&Phi;200</td><td>1,200</td><td>706</td><td>380</td><td>120</td><td>45&ndash;50</td><td>4</td><td>0.097</td><td>14.00</td></tr>
  <tr><td><strong>BXF-250</strong></td><td>&Phi;250</td><td>1,800</td><td>1,060</td><td>488</td><td>200</td><td>54&ndash;60</td><td>1</td><td>0.043</td><td>7.35</td></tr>
  <tr><td><strong>BXF-315</strong></td><td>&Phi;315</td><td>2,200</td><td>1,295</td><td>693</td><td>330</td><td>60&ndash;70</td><td>1</td><td>0.072</td><td>9.15</td></tr>
  </table>
  </div>
  <p class="tnote">معلنة عند 220-240V / 50Hz بسحب وطرد حرّين. نسخ 60Hz للسعودية والإمارات والكويت وقطر، و110V / 60Hz لأمريكا الشمالية، تُنتج حسب الطلب. الوزن الصافي يعتمد على اللف ومجموعة الكبلات &mdash; ويُعتمد في قائمة التعبئة لكل طلب.</p>

  <span class="section-tag">التركيب</span>
  <h2 class="sec">تفاصيل تحدد إن كان النظام سيعمل</h2>
  <div class="appgrid">
      <div class="appcard"><h4>الفلتر على الهود والمروحة عند الطرد</h4><p>فلتر حاجزي من الستيل داخل المظلة، ثم المروحة بعده وخارج مساحة الطهي. لا داخل المظلة أبداً، ولا داخل مسار قناة دهون.</p></div>
      <div class="appcard"><h4>اترك منفذاً للتنظيف</h4><p>فتحة تنظيف قبل المروحة وبعدها. حتى الخط المفلتر يغطي الدفاعة بطبقة خلال موسم، والدفاعة غير المتوازنة تصبح مطالبة ضمان.</p></div>
      <div class="appcard"><h4>وصلات مرنة على الجانبين</h4><p>جلبتان مرنتان وقواعد مانعة للاهتزاز إذا كانت المروحة معلقة فوق سقف &mdash; هذا ما يمنع وصول دمدمة المطبخ إلى صالة الطعام.</p></div>
      <div class="appcard"><h4>ميل القناة إلى المصرف</h4><p>أمل المسار راجعاً نحو الهود أو نقطة تصريف حتى لا تتجمع المياه المتكثفة ومياه التنظيف داخل المروحة.</p></div>
      <div class="appcard"><h4>قاطع فصل في مرمى النظر</h4><p>قاطع محلي قرب المروحة لأعمال الصيانة. ومحرك IP44 لمناطق الغسل وطرد غسيل الأطباق.</p></div>
      <div class="appcard"><h4>هواء التعويض بعيداً عن الهود</h4><p>أدخِله من مستوى منخفض في الجانب المقابل للغرفة. نفخ الإمداد عبر واجهة الهود يفسد الاحتجاز ويدفع الدهون إلى داخل الغرفة.</p></div>
  </div>

  <span class="section-tag">مواضيع ذات صلة</span>
  <h2 class="sec">المواصفات وقراءات أخرى</h2>
  <div class="fgrid">
    <a class="fcard" href="https://baer-ventilation.com/ar/product-inline-duct-fan"><h4>سلسلة BXF &mdash; المواصفات الكاملة وطلب العرض</h4></a>
    <a class="fcard" href="https://baer-ventilation.com/inline-duct-fan-vs-axial-fan"><h4>مروحة قناة أم مروحة محورية</h4></a>
    <a class="fcard" href="https://baer-ventilation.com/exhaust-fan-airflow-calculation-guide"><h4>كيف تحسب تدفق الهواء المطلوب</h4></a>
    <a class="fcard" href="https://baer-ventilation.com/exhaust-fan-noise-levels-guide"><h4>شرح مستويات ضجيج المراوح (dB A)</h4></a>
    <a class="fcard" href="https://baer-ventilation.com/exhaust-fan-moq-guide"><h4>الحد الأدنى للطلب والمخزون وكميات OEM</h4></a>
    <a class="fcard" href="https://baer-ventilation.com/industrial-exhaust-fans"><h4>مراوح عادم صناعية للقاعات والورش</h4></a>
  </div>

  <h2 class="sec">الشهادات والمصنع</h2>
  <p style="max-width:900px;">شهادة CE قياسية &mdash; رقم <strong>XH2601E0321945GC</strong> (Xihua International Testing &amp; Certification، شنتشن)، صالحة حتى 2031-01-28. والمصنع حاصل على ISO 9001 (<strong>04625Q15304R1M</strong>) وCCC (<strong>2024010702612682</strong>). ويمكن ترتيب ETL عند الطلب للتوزيع في الولايات المتحدة؛ أما شهادة SAA لأستراليا فتُجدَّد لكل طلب ولا تُحتفظ بها حالياً. كل الأرقام منشورة لتتحقق منها في <a href="https://baer-ventilation.com/ar/verify/" style="color:#C0392B;font-weight:700;text-decoration:none;">صفحة التحقق من الشهادات</a>.</p>
  <p style="max-width:900px;"><strong>أين تُصنع.</strong> أربع ورش، و50,000 م&sup2; من مباني الإنتاج، واثنتا عشرة ماكينة حقن وثمانية خطوط تجميع في شنغتشو بمقاطعة تشجيانغ &mdash; راجع <a href="https://baer-ventilation.com/baer-production-capacity" style="color:#C0392B;font-weight:700;text-decoration:none;">صفحة المصنع والطاقة الإنتاجية</a>.</p>

  <span class="section-tag">أسئلة المشترين</span>
  <h2 class="sec">الأسئلة الشائعة</h2>
  <div class="faqwrap">
      <details><summary>هل يمكن استخدام مروحة قناة BXF لهود مطعم؟ <span>+</span></summary><div class="fa">نعم، مع خط التركيب المناسب. للطهي الخفيف &mdash; أفران كهربائية وأفران وصواني تسخين ومعدات حفظ ساخن &mdash; فإن BXF خلف فلتر حاجزي من الستيل ومركّبة عند نهاية الطرد خيار طبيعي ومجدٍ. وللقلايات العميقة وقدور الووك والشوّابات فهي مستخدمة على نطاق واسع أيضاً في الشرق الأوسط وجنوب شرق آسيا، بشرطين: غسل الدفاعة كل موسم، وأن تكون المروحة خارج مساحة الطهي في نهاية المسار حتى لا تلتصق الدهون عليها بالحرارة. وإذا كان المشروع معتمداً وفق كود حريق يفرض مروحة معتمدة للدهون ومحركاً خارج مسار الهواء، فاتبع الكود &mdash; أرسل لنا البند وسنخبرك بما يحتاجه التركيب قبل الطلب.</div></details>
      <details><summary>كم تدفق هواء يحتاجه مطبخي؟ <span>+</span></summary><div class="fa">ابدأ من الهود: 100 CFM لكل قدم طولي من واجهة الهود للحمل الخفيف، و200 للمتوسط، و300 للثقيل. اضرب في 1.7 لتحصل على m&sup3;/h، ثم أضف 20% للفلتر والأكواع وشبك الجدار. هود بطول 2.4 م بحمل متوسط يعطي نحو 3,260 m&sup3;/h &mdash; أي وحدتان BXF-250 على التوازي. أرسل أبعاد الغرفة والهود ونحسبها لك.</div></details>
      <details><summary>مروحة واحدة أم عدة مراوح على التوازي؟ <span>+</span></summary><div class="fa">الوحدات على التوازي أمر طبيعي فوق نحو 2,500 m&sup3;/h. وحدتان في غرفة تجميع مشتركة تمنحان احتياطاً &mdash; يمكن للمطبخ أن يستمر في العمل بواحدة أثناء صيانة الأخرى &mdash; كما أن تفريعات القنوات أسهل في التمديد من مروحة كبيرة واحدة. حافظ على تماثل الفروع، وإلا هيمنت المروحة الأقوى على التدفق.</div></details>
      <details><summary>هل أحتاج هواء تعويض فعلاً؟ <span>+</span></summary><div class="fa">نعم، نحو 85% من حجم الطرد. المطبخ المغلق يخنق مروحة الطرد: قد ينخفض التدفق المعلن بمقدار الثلث، ويفقد الهود قدرته على احتجاز الدهون والبخار، وتصبح الأبواب صعبة الفتح، ويمكن أن ترتد أجهزة الغاز أول أكسيد الكربون إلى الغرفة. ويجب إدخال الإمداد بعيداً عن واجهة الهود، والأفضل من مستوى منخفض في الجدار المقابل.</div></details>
      <details><summary>هل هي هادئة بما يكفي قرب صالة الطعام؟ <span>+</span></summary><div class="fa">تعمل BXF-100 إلى BXF-150 عند 28&ndash;32 dB(A)، أي أهدأ من محادثة عادية. أما المقاسات 200&ndash;315 فتعمل عند 45&ndash;70 dB(A) ولا ينبغي أن تشترك في الجدار مع أماكن الجلوس. ثلاثة أمور تحل الضجيج: تركيب المروحة خارج المساحة المشغولة، ووصلات مرنة، وقناة بمقاس أكبر درجة واحدة مع مخفّض عند المروحة.</div></details>
      <details><summary>هل توفرون نسخ 60Hz أو 110V؟ <span>+</span></summary><div class="fa">نعم. 220-240V / 50Hz هو القياسي. ونسخ 60Hz للسعودية والإمارات والكويت وقطر والعراق، و110V / 60Hz للولايات المتحدة وكندا، تُبنى حسب الطلب &mdash; اذكر الجهد في الاستفسار ليُدرج في العرض. ووحدات 60Hz تدور أسرع بنحو 20% مع تدفق وضغط وضجيج أعلى نسبياً.</div></details>
      <details><summary>ما الحد الأدنى للطلب ومدة التسليم؟ <span>+</span></summary><div class="fa">الحد الأدنى 100 قطعة لكل طراز لطلبات الإنتاج؛ ويمكن توريد وحدات مفردة كعينات بسعر العينة مع تحمّل المشتري أجرة الشحن. والإنتاج الكمي يستغرق 25&ndash;35 يوماً من الدفعة المقدمة واعتماد التصميم. والتعبئة كرتون كرافت محايد افتراضياً، مع كراتين مطبوعة ملوّنة مجاناً فوق 1,000 قطعة لكل طراز.</div></details>
      <details><summary>هل تورّدون الهود والفلاتر والقنوات؟ <span>+</span></summary><div class="fa">لا &mdash; نحن نصنع المراوح. الهودات والفلاتر الحاجزية والقنوات يورّدها صانع مطبخك أو المقاول المحلي، ونحن نحجّم المروحة على أرقامهم. أرسل لنا رسم الهود ومسار القناة ونؤكد الطراز وهامش الضغط وسرعة القناة، وننبّه إلى أي شيء لن يعمل قبل أن تطلب.</div></details>
  </div>

  <div class="ctabox">
    <h2>أرسل طول الهود ومسار القناة</h2>
    <p>أخبرنا بطول الهود، ومعدات الطهي تحته، وطول القناة وعدد الأكواع، والجهد الكهربائي، وميناء الوصول. نرد بالتدفق الذي تحتاجه، والطراز الذي يحققه عند ذلك الضغط، وعرض سعر رسمي &mdash; خلال 24 ساعة.</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="https://wa.me/8613655859122" target="_blank">واتساب: +86 136 5585 9122</a>
      <a class="btn btn-red" href="https://baer-ventilation.com/ar/contact/">أرسل استفساراً</a>
      <a class="btn btn-ghost" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a>
    </div>
  </div>

</div>
"""

FOOTER = """
<footer>
  <div class="fgrid">
    <div>
      <a href="https://baer-ventilation.com/ar/" class="logo">BAER<span>VENT</span></a>
      <p style="margin-top:14px;">إنتاج مراوح التهوية عالمياً منذ 2003. من قاعدتنا البالغة 50,000 م&sup2; من مباني الإنتاج في شنغتشو، تشجيانغ، الصين &mdash; معتمدة CE / ISO 9001 / 3C / CB. ويمكن ترتيب SAA وETL عند الطلب.</p>
    </div>
    <div>
      <h4>روابط سريعة</h4>
      <ul>
        <li><a href="https://baer-ventilation.com/ar/">الرئيسية</a></li>
        <li><a href="https://baer-ventilation.com/ar/products/">المنتجات</a></li>
        <li><a href="https://baer-ventilation.com/ar/about/">من نحن</a></li>
        <li><a href="https://baer-ventilation.com/ar/contact/">اتصل بنا</a></li>
        <li><a href="https://baer-ventilation.com/baer-fan-catalog.pdf" target="_blank">كتالوج PDF</a></li>
      </ul>
    </div>
    <div>
      <h4>معلومات التواصل</h4>
      <p><a class="fmail" href="mailto:sunny@zjbaer.com">sunny@zjbaer.com</a></p>
      <p>WhatsApp / WeChat: +86 136 5585 9122</p>
      <p>8-1 Jingwu Road, Ganlin Town, Shengzhou City, Shaoxing City, Zhejiang Province, China</p>
    </div>
  </div>
  <div class="copy">© 2026 Zhejiang Baer Electrical Technology Co., Ltd. (BAER Ventilation) &mdash; جميع الحقوق محفوظة.</div>

<div style="text-align:center;font-size:12px;opacity:.85;padding-top:8px;">&#9654; <a href="https://www.youtube.com/@BAERVentilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">YouTube @BAERVentilation</a> &middot; <a href="https://www.linkedin.com/company/baer-ventilation" target="_blank" rel="noopener" style="color:#E21E26;text-decoration:none;">LinkedIn</a></div>
  <p style="margin:14px 0 0;font-size:12px;opacity:.85;"><a href="/privacy/" style="color:inherit;text-decoration:underline;">سياسة الخصوصية</a> &middot; <a href="/privacy/#cookies" style="color:inherit;text-decoration:underline;">ملفات تعريف الارتباط</a> &middot; <a href="https://baer-ventilation.com/ar/verify/" style="color:inherit;text-decoration:underline;">تحقّق من شركتنا</a></p>
</footer>

<div class="floating">
  <a href="https://wa.me/8613655859122" target="_blank" class="float-btn fb-wa" aria-label="WhatsApp">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://baer-ventilation.com/baer-fan-catalog.pdf" target="_blank" class="float-btn fb-pdf" aria-label="كتالوج PDF">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
  </a>
  <a href="https://baer-ventilation.com/ar/contact/" class="float-btn fb-q" aria-label="اطلب عرض سعر">
    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </a>
</div>

<!-- GA4 conversion events: WhatsApp / email / PDF catalog / phone / form -->
<script>
function _baerGtagCtx(){ return { page_path: window.location.pathname, page_title: document.title }; }
document.addEventListener('click', function(e){
  var t = e.target;
  while (t && t !== document.body && t.tagName !== 'A') { t = t.parentElement; }
  if (!t || t.tagName !== 'A' || typeof gtag !== 'function') return;
  var href = t.getAttribute('href') || '';
  var ctx = _baerGtagCtx();
  ctx.link_text = (t.textContent || '').trim().slice(0, 120);
  ctx.link_url = href;
  if (/wa\\.me|whatsapp/i.test(href)) { gtag('event', 'whatsapp_click', ctx); }
  else if (href.indexOf('mailto:') === 0) { gtag('event', 'email_click', ctx); }
  else if (/\\.pdf(\\?|$)/i.test(href)) { ctx.file_name = href.split('/').pop().split('?')[0]; gtag('event', 'catalog_download', ctx); }
  else if (href.indexOf('tel:') === 0) { gtag('event', 'phone_click', ctx); }
});
</script>

<script src="/js/reveal.js?v=1" defer></script>
<script type="application/ld+json">{"@context": "https://schema.org", "@graph": [{"@type": ["WebPage", "CollectionPage"], "@id": "URL_AR", "url": "URL_AR", "name": "مراوح عادم المطابخ التجارية: أنظمة قنوات مختلطة التدفق", "description": "مراوح عادم مطابخ تجارية مختلطة التدفق من 290 إلى 2,200 m3/h وحتى 693 Pa للمقاهي والمطاعم والكافيتيريا وغسيل الأطباق، مع تحجيم بطول الهود وسرعة القناة وميزانية الضغط.", "isPartOf": {"@id": "https://baer-ventilation.com/#website"}, "inLanguage": "ar", "dateModified": "2026-11-03", "breadcrumb": {"@id": "URL_AR#breadcrumb"}}]}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": "URL_AR#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "https://baer-ventilation.com/ar/"}, {"@type": "ListItem", "position": 2, "name": "المنتجات", "item": "https://baer-ventilation.com/ar/products/"}, {"@type": "ListItem", "position": 3, "name": "مراوح عادم المطابخ التجارية", "item": "URL_AR"}]}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "@id": "URL_AR#faq", "inLanguage": "ar", "mainEntity": [{"@type": "Question", "name": "هل يمكن استخدام مروحة قناة BXF لهود مطعم؟", "acceptedAnswer": {"@type": "Answer", "text": "نعم، مع خط التركيب المناسب. للطهي الخفيف مثل الأفران الكهربائية والصواني ومعدات الحفظ الساخن، فإن BXF خلف فلتر حاجزي من الستيل ومركبة عند نهاية الطرد خيار طبيعي ومجد. وللقلايات العميقة وقدور الووك والشوّابات فهي مستخدمة على نطاق واسع في الشرق الأوسط وجنوب شرق آسيا، بشرطين: غسل الدفاعة كل موسم، وأن تكون المروحة خارج مساحة الطهي في نهاية المسار. وحيث يفرض الكود مروحة معتمدة للدهون ومحركا خارج مسار الهواء، فاتبع الكود."}}, {"@type": "Question", "name": "كم تدفق هواء يحتاجه مطبخي؟", "acceptedAnswer": {"@type": "Answer", "text": "احسب 100 CFM لكل قدم طولي من واجهة الهود للحمل الخفيف، و200 للمتوسط، و300 للثقيل، ثم اضرب في 1.7 للحصول على m3/h، وأضف 20% للفلتر والأكواع وشبك الجدار. هود بطول 2.4 م بحمل متوسط يعطي نحو 3,260 m3/h أي وحدتين BXF-250 على التوازي."}}, {"@type": "Question", "name": "هل أحتاج هواء تعويض؟", "acceptedAnswer": {"@type": "Answer", "text": "نعم، نحو 85% من حجم الطرد. من دونه تختنق مروحة الطرد وقد ينخفض التدفق بمقدار الثلث، ويفقد الهود احتجازه، وتصبح الأبواب صعبة الفتح، ويمكن أن ترتد أجهزة الغاز."}}, {"@type": "Question", "name": "ما سرعة القناة المناسبة لطرد المطبخ؟", "acceptedAnswer": {"@type": "Answer", "text": "7.6 إلى 10 م/ث (1,500 إلى 2,000 fpm) لقناة الدهون لإبقاء الرواسب متحركة، و5 إلى 8 م/ث للطرد العام. BXF-315 في قناة 315 مم تعمل عند 7.8 م/ث عند التدفق المعلن، والمقاسات 100 إلى 250 تعمل عند 9.5 إلى 10.6 م/ث وهي مناسبة للمسارات القصيرة."}}, {"@type": "Question", "name": "هل هي هادئة بما يكفي قرب صالة الطعام؟", "acceptedAnswer": {"@type": "Answer", "text": "تعمل BXF-100 إلى BXF-150 عند 28 إلى 32 dB(A)، أي أهدأ من محادثة عادية. والمقاسات 200 إلى 315 تعمل عند 45 إلى 70 dB(A). ركب المروحة خارج المساحة المشغولة، واستخدم وصلات مرنة، وقناة بمقاس أكبر درجة واحدة لتخفيض الضجيج."}}, {"@type": "Question", "name": "هل توفرون نسخ 60Hz أو 110V؟", "acceptedAnswer": {"@type": "Answer", "text": "نعم. 220-240V / 50Hz قياسي، ونسخ 60Hz للسعودية والإمارات والكويت وقطر والعراق، و110V / 60Hz لأمريكا الشمالية، تبنى حسب الطلب."}}, {"@type": "Question", "name": "ما الحد الأدنى للطلب ومدة التسليم؟", "acceptedAnswer": {"@type": "Answer", "text": "الحد الأدنى 100 قطعة لكل طراز لطلبات الإنتاج. العينات بسعر العينة مع تحمل المشتري أجرة الشحن. الإنتاج الكمي يستغرق 25 إلى 35 يوما من الدفعة المقدمة واعتماد التصميم، والتعبئة كرتون كرافت محايد افتراضيا مع كراتين مطبوعة مجانا فوق 1,000 قطعة لكل طراز."}}, {"@type": "Question", "name": "هل تورّدون الهود والفلاتر والقنوات؟", "acceptedAnswer": {"@type": "Answer", "text": "لا، نحن نصنع المراوح. الهودات والفلاتر والقنوات يوردها صانع المطبخ أو المقاول المحلي، ونحن نحجم المروحة على أرقامهم ونؤكد الطراز وهامش الضغط وسرعة القناة قبل الطلب."}}]}</script>
</body>
</html>
"""

# ---------- bidi fixes: Latin/number runs inside RTL text ----------
# Empirically verified (Chrome): numeric ranges "290-2,200", "693 Pa", dates
# "2031-01-28", "+86 136 5585 9122" and "220-240V / 50Hz" all render REVERSED
# in RTL paragraphs unless isolated with dir="ltr". "BXF-315", "ISO 9001",
# certificate numbers and bare Arabic-unit pairs ("7.8 m/s") are safe.

UNIT = r"(?:m&sup3;/h|dB\(A\)|CFM|Pa|fpm|Hz|W|mm)"

def _ltr(m):
    return '<span dir="ltr">' + m.group(1) + "</span>"

def fix_bidi(html, pct=True):
    # whole-formula chains first so the generic rules never split them
    html = html.replace(
        "200 CFM = <strong>1,600 CFM = 2,715 m&sup3;/h</strong>",
        '<strong><span dir="ltr">200 CFM = 1,600 CFM = 2,715 m&sup3;/h</span></strong>')
    html = html.replace(
        "1 CFM = 1.7 m&sup3;/h",
        '<span dir="ltr">1 CFM = 1.7 m&sup3;/h</span>')
    # numeric range, optionally followed by a Latin unit
    html = re.sub(
        r"(\d[\d,]*(?:\.\d+)?&ndash;\d[\d,]*(?:\.\d+)?(?: " + UNIT + r")?)", _ltr, html)
    # single number + Latin unit
    html = re.sub(r"(\d[\d,]*(?:\.\d+)? " + UNIT + r")", _ltr, html)
    # percent values (text only; never applied to attributes/URLs — the
    # encoded wa.me?text= href in TOPBAR must stay untouched)
    if pct:
        html = re.sub(r"(\d[\d,]*%)", _ltr, html)
    # literal tokens that reverse in RTL
    for token in ["220-240V / 50Hz", "110V / 60Hz", "2031-01-28", "+86 136 5585 9122"]:
        html = html.replace(token, '<span dir="ltr">' + token + "</span>")
    return html

BODY1 = fix_bidi(BODY1)
BODY2 = fix_bidi(BODY2)
TOPBAR = fix_bidi(TOPBAR, pct=False)
FOOTER = FOOTER.replace("+86 136 5585 9122", '<span dir="ltr">+86 136 5585 9122</span>')

html = HEAD + TOPBAR + BODY1 + BODY2 + FOOTER
html = html.replace("URL_AR", URL_AR)

# CRLF like the rest of the repo
html = html.replace("\r\n", "\n").replace("\n", "\r\n")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "wb").write(html.encode("utf-8"))

words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)).split())
print("written", OUT)
print("bytes", len(html.encode("utf-8")), "words", words)
print("h2", html.count("<h2"), "| details", html.count("<details"), "| tables", html.count("<table"))
