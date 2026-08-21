/* ============================================================
   BAER Ventilation — main.js
   Hero slider · Counter · Mobile menu · Lang dropdown · Modal
   ============================================================ */

(function () {
  'use strict';

  /* ── Navbar scroll shadow ── */
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', function () {
      navbar.classList.toggle('scrolled', window.scrollY > 10);
    });
  }

  /* ── Mobile hamburger menu ── */
  const toggle   = document.getElementById('mobile-menu');
  const navLinks = document.getElementById('nav-links');
  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      toggle.classList.toggle('active');
      navLinks.classList.toggle('open');
    });
  }

  /* ── Language dropdown ── */
  const langBtn     = document.getElementById('lang-btn');
  const langContent = document.getElementById('lang-content');
  if (langBtn && langContent) {
    langBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      langContent.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      langContent.classList.remove('open');
    });
  }

  /* ── Hero Slider ── */
  (function initSlider() {
    const slides = document.querySelectorAll('.hero-slider .slide');
    const dots   = document.querySelectorAll('.slider-dots .dot');
    if (!slides.length) return;

    let current  = 0;
    let timer    = null;
    const DELAY  = 4500;

    function goTo(index) {
      slides[current].classList.remove('active');
      dots[current] && dots[current].classList.remove('active');
      current = (index + slides.length) % slides.length;
      slides[current].classList.add('active');
      dots[current] && dots[current].classList.add('active');
    }

    function next() { goTo(current + 1); }

    function startAuto() {
      clearInterval(timer);
      timer = setInterval(next, DELAY);
    }

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        goTo(i);
        startAuto();
      });
    });

    goTo(0);
    startAuto();
  })();

  /* ── Counter animation ── */
  (function initCounters() {
    const counters = document.querySelectorAll('.js-counter');
    if (!counters.length) return;

    function animateCounter(el) {
      const target   = parseInt(el.dataset.target, 10);
      const duration = 1800;
      const step     = 16;
      const steps    = Math.ceil(duration / step);
      let   count    = 0;

      const inc = setInterval(function () {
        count++;
        el.textContent = Math.round((target * count) / steps);
        if (count >= steps) {
          el.textContent = target;
          clearInterval(inc);
        }
      }, step);
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    counters.forEach(function (el) { observer.observe(el); });
  })();

  /* ── Product Modal (multilingual) ── */

  /* spec label translations: key → [en, ar, zh] */
  var specLabels = {
    'Size':            ['Size',            'المقاس',           '尺寸'],
    'Airflow':         ['Airflow',         'تدفق الهواء',      '风量'],
    'Noise':           ['Noise',           'مستوى الضوضاء',    '噪音'],
    'Power':           ['Power',           'الطاقة',           '功率'],
    'Voltage':         ['Voltage',         'الجهد الكهربائي',  '电压'],
    'Certification':   ['Certification',   'الشهادات',         '认证'],
    'Static Pressure': ['Static Pressure', 'الضغط الستاتيكي',  '静压'],
    'IP Rating':       ['IP Rating',       'درجة الحماية IP',  'IP防护等级'],
    'Motor':           ['Motor',           'المحرك',           '电机'],
    'Energy Saving':   ['Energy Saving',   'توفير الطاقة',     '节能'],
    'Control':         ['Control',         'التحكم',           '控制方式'],
    'Filter':          ['Filter',          'الفلتر',           '过滤器'],
    'Heat Recovery':   ['Heat Recovery',   'استعادة الحرارة',  '热回收效率'],
    'Application':     ['Application',     'التطبيقات',        '应用场景'],
    'Switch':          ['Switch',          'مفتاح التشغيل',    '开关方式'],
    'MOQ':             ['MOQ',             'الحد الأدنى للطلب','最小起订量']
  };

  /* inquiry button label per language */
  var inquireLabel = {
    en: 'Inquire Now',
    ar: 'استفسر الآن',
    zh: '立即询盘'
  };

  /* productData: each entry has img + per-language title/desc/specs */
  var productData = {
    p1: {
      img: 'https://sc02.alicdn.com/kf/H5ab785de74ed4850a9fbf3621c91530cH.jpg',
      en: { title: 'Ceiling Mount Exhaust Fan',
            desc:  'Energy-efficient ceiling-mounted exhaust fan designed for residential and light-commercial applications. Features low-noise motor, automatic shutter, and easy grid installation.',
            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']] },
      ar: { title: 'مروحة شفط سقفية',
            desc:  'مروحة شفط سقفية موفرة للطاقة مصممة للاستخدامات السكنية والتجارية الخفيفة. تتميز بمحرك منخفض الضوضاء وغالق تلقائي وتركيب شبكي سهل.',
            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']] },
      zh: { title: '吸顶换气扇',
            desc:  '节能吸顶式换气扇，专为住宅及轻商业场所设计。具备低噪音电机、自动百叶和简易格栅安装功能。',
            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']] }
    },
    p2: {
      img: 'https://sc02.alicdn.com/kf/H5fbe6fbc92284181968eba3dff7ed880E.jpg',
      en: { title: 'Standard Window Fan',
            desc:  'Classic window-mounted exhaust fan suitable for kitchens, bathrooms, and small workshops. Durable ABS housing with anti-back-draft shutter.',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']] },
      ar: { title: 'مروحة نافذة قياسية',
            desc:  'مروحة شفط كلاسيكية مثبتة على النافذة مناسبة للمطابخ والحمامات والورش الصغيرة. هيكل ABS متين مع غالق مضاد للتدفق العكسي.',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']] },
      zh: { title: '标准窗式换气扇',
            desc:  '经典窗式安装换气扇，适用于厨房、卫浴及小型工作间。耐用ABS外壳，配备防回流百叶。',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']] }
    },
    p3: {
      img: 'https://sc02.alicdn.com/kf/A216d65f6e04a43438a882ca3e9b88721Z.png',
      en: { title: 'Double-Grill Window Fan',
            desc:  'Two-layer grille design for improved airflow direction control. Ideal for through-wall installation in residential and commercial buildings.',
            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']] },
      ar: { title: 'مروحة نافذة مزدوجة الشبك',
            desc:  'تصميم شبكي مزدوج لتحسين التحكم في اتجاه تدفق الهواء. مثالية للتركيب في الجدران للمباني السكنية والتجارية.',
            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']] },
      zh: { title: '双格栅窗式换气扇',
            desc:  '双层格栅设计，有效改善气流方向控制。适合住宅及商业建筑穿墙安装。',
            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']] }
    },
    p4: {
      img: 'https://sc02.alicdn.com/kf/H42e66ea71d5445fcbb62c7c68e493d94v.jpg',
      en: { title: 'Industrial Axial Fan',
            desc:  'Heavy-duty axial fan for industrial ventilation. High static pressure, continuous duty, IP55 rated for harsh environments.',
            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']] },
      ar: { title: 'مروحة محورية صناعية',
            desc:  'مروحة محورية للأعمال الشاقة للتهوية الصناعية. ضغط ستاتيكي عالٍ، تشغيل مستمر، مقاومة IP55 للبيئات القاسية.',
            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']] },
      zh: { title: '工业轴流风机',
            desc:  '重型轴流风机，适用于工业通风场合。高静压，可连续运行，IP55防护等级，耐恶劣环境。',
            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']] }
    },
    p5: {
      img: 'https://sc02.alicdn.com/kf/Hf77c8f2216ff4576b9f83c896fdd000fq.jpg',
      en: { title: 'Standard Mixed Flow Series',
            desc:  'Inline duct fan combining axial and centrifugal design for high airflow with moderate static pressure. Suitable for residential HRV and HVAC duct systems.',
            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']] },
      ar: { title: 'سلسلة التدفق المختلط القياسي',
            desc:  'مروحة قناة مدمجة تجمع بين التصميم المحوري والطرد المركزي لتدفق هواء عالٍ مع ضغط ستاتيكي معتدل. مناسبة لأنظمة HRV السكنية وقنوات HVAC.',
            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']] },
      zh: { title: '标准斜流管道风机',
            desc:  '管道内嵌式风机，融合轴流与离心设计，高风量、中等静压。适用于住宅新风系统及暖通管道。',
            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']] }
    },
    p7: {
      img: 'https://sc02.alicdn.com/kf/A69a6450d8e504c9a9c1dcaedccad5c3e2.png',
      en: { title: 'High-Efficiency Booster Fan',
            desc:  'Mixed flow booster for long duct runs. High static pressure overcomes resistance in complex HVAC systems.',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']] },
      ar: { title: 'معزز تدفق عالي الكفاءة',
            desc:  'معزز تدفق مختلط لمسارات القنوات الطويلة. ضغط ستاتيكي عالٍ يتغلب على مقاومة أنظمة HVAC المعقدة.',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']] },
      zh: { title: '高效助推风机',
            desc:  '斜流助推风机，适用于长管道场合。超高静压，克服复杂暖通系统阻力。',
            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']] }
    },
    p8: {
      img: 'https://sc02.alicdn.com/kf/A96cb71eed6d94b289be81e750dfc9fe1M.png',
      en: { title: 'Intelligent DC Inverter Fan',
            desc:  'DC brushless motor with variable speed control. Up to 60% energy saving vs AC equivalents. Smart humidity / CO₂ trigger available.',
            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','DC Brushless'],['Energy Saving','Up to 60%'],['Control','PWM / 0-10V / Smart Sensor']] },
      ar: { title: 'مروحة عاكس DC الذكية',
            desc:  'محرك بدون فرش DC مع تحكم في السرعة المتغيرة. توفير طاقة يصل إلى 60% مقارنة بنظيراتها AC. متوفر مع مشغل رطوبة / CO₂ ذكي.',
            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','DC بدون فرش'],['Energy Saving','حتى 60%'],['Control','PWM / 0-10V / حساس ذكي']] },
      zh: { title: '智能直流变频风机',
            desc:  '直流无刷电机，无级变速控制。比同规格交流产品节能最高60%。可选配湿度/CO₂智能触发。',
            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','直流无刷'],['Energy Saving','最高节能60%'],['Control','PWM / 0-10V / 智能传感器']] }
    },
    p9: {
      img: 'https://sc02.alicdn.com/kf/H0f20bd34e6864282a2d71d6aa8f11a35f.jpg',
      en: { title: 'Export Pro Bathroom Series',
            desc:  'Complete bathroom exhaust fan range covering ceiling, wall, and window-mounted configurations. CE certified, designed specifically for Middle East and European export markets.',
            specs: [['Airflow','50~220 m³/h'],['Noise','≤28 dB(A)'],['IP Rating','IP44 (bathroom safe)'],['Certification','CE, RoHS'],['MOQ','500 pcs']] },
      ar: { title: 'سلسلة حمامات التصدير الاحترافية',
            desc:  'مجموعة كاملة من مراوح شفط الحمامات تشمل التركيب في السقف والجدار والنافذة. معتمدة CE، مصممة خصيصاً لأسواق التصدير في الشرق الأوسط وأوروبا.',
            specs: [['Airflow','50~220 m³/h'],['Noise','≤28 dB(A)'],['IP Rating','IP44 (مقاوم للرطوبة)'],['Certification','CE, RoHS'],['MOQ','500 قطعة']] },
      zh: { title: '出口专业卫浴系列',
            desc:  '完整卫浴换气扇系列，涵盖吸顶、壁装和窗装款式。CE认证，专为中东及欧洲出口市场设计。',
            specs: [['Airflow','50~220 m³/h'],['Noise','≤28 dB(A)'],['IP Rating','IP44（浴室安全）'],['Certification','CE, RoHS'],['MOQ','500件起订']] }
    },
    'p3-n2': {
      img: 'https://sc02.alicdn.com/kf/Abe879211958d43a4996a2f163a09d541e.png',
      en: { title: 'Circular Pull-Cord Fan',
            desc:  'Classic round panel design with convenient pull-cord switch. Perfect for bathrooms and kitchens without wall switches. Compact and easy to install.',
            specs: [['Size','100mm / 150mm'],['Airflow','60~140 m³/h'],['Noise','≤26 dB(A)'],['Power','8~18 W'],['Switch','Pull-cord']] },
      ar: { title: 'مروحة دائرية بسلسلة سحب',
            desc:  'تصميم لوحة دائري كلاسيكي مع مفتاح سلسلة سحب مريح. مثالية للحمامات والمطابخ التي لا تحتوي على مفاتيح حائط. مدمجة وسهلة التركيب.',
            specs: [['Size','100mm / 150mm'],['Airflow','60~140 m³/h'],['Noise','≤26 dB(A)'],['Power','8~18 W'],['Switch','سلسلة سحب']] },
      zh: { title: '圆型拉绳换气扇',
            desc:  '经典圆形面板设计，配备便捷拉绳开关。特别适合没有墙壁开关的卫浴和厨房。体积小巧，安装简便。',
            specs: [['Size','100mm / 150mm'],['Airflow','60~140 m³/h'],['Noise','≤26 dB(A)'],['Power','8~18 W'],['Switch','拉绳开关']] }
    },
    p10: {
      img: 'https://sc02.alicdn.com/kf/Hb4c5e8471a3e46d599e56f223890a1d36.jpg',
      en: { title: 'Acoustic Cabinet Fan',
            desc:  'Ultra-quiet inline fan engineered for server cabinet, home cinema, and bedroom applications. Double-skin acoustic lining reduces noise to exceptional levels.',
            specs: [['Size','100mm / 125mm / 150mm'],['Airflow','80~450 m³/h'],['Noise','≤18 dB(A)'],['Motor','DC Brushless'],['Application','Cabinet / Studio / Bedroom']] },
      ar: { title: 'مروحة خزانة صوتية',
            desc:  'مروحة مدمجة فائقة الهدوء مصممة لخزانات الخوادم وسينما المنازل وتطبيقات غرف النوم. البطانة الصوتية المزدوجة تقلل الضوضاء إلى مستويات استثنائية.',
            specs: [['Size','100mm / 125mm / 150mm'],['Airflow','80~450 m³/h'],['Noise','≤18 dB(A)'],['Motor','DC بدون فرش'],['Application','خزانة / ستوديو / غرفة نوم']] },
      zh: { title: '静音机柜风机',
            desc:  '超静音管道内嵌式风机，专为服务器机柜、家庭影院和卧室设计。双层吸音内衬，将噪音降至极低水平。',
            specs: [['Size','100mm / 125mm / 150mm'],['Airflow','80~450 m³/h'],['Noise','≤18 dB(A)'],['Motor','直流无刷'],['Application','机柜 / 录音室 / 卧室']] }
    },
    p13: {
      img: 'https://sc02.alicdn.com/kf/Ac07b0ea4758d43eca21098ba7444ee35Q.png',
      en: { title: 'Fresh Air Purification Unit',
            desc:  'Integrated ERV unit with H13 HEPA + activated carbon filter. Provides fresh air intake while recovering heat/cooling, ideal for sealed modern buildings.',
            specs: [['Airflow','150~350 m³/h'],['Filter','H13 HEPA + Activated Carbon'],['Heat Recovery','Up to 85%'],['Noise','≤32 dB(A)'],['Application','Apartment / Office / Clinic']] },
      ar: { title: 'وحدة تنقية الهواء النقي',
            desc:  'وحدة ERV متكاملة مع فلتر HEPA H13 + كربون نشط. توفر تدفق هواء نقي مع استعادة الحرارة/التبريد، مثالية للمباني الحديثة المغلقة.',
            specs: [['Airflow','150~350 m³/h'],['Filter','HEPA H13 + كربون نشط'],['Heat Recovery','حتى 85%'],['Noise','≤32 dB(A)'],['Application','شقة / مكتب / عيادة']] },
      zh: { title: '新风净化机组',
            desc:  '集成ERV全热交换机组，配备H13 HEPA+活性炭过滤器。在回收热/冷量的同时引入新鲜空气，适合密封型现代建筑。',
            specs: [['Airflow','150~350 m³/h'],['Filter','H13 HEPA + 活性炭'],['Heat Recovery','最高85%'],['Noise','≤32 dB(A)'],['Application','公寓 / 办公室 / 诊所']] }
    }
  };

  /* track current language (default en) */
  var currentLang = 'en';

  window.openProductModal = function (id) {
    var entry = productData[id];
    if (!entry) return;

    var overlay = document.getElementById('product-modal');
    var content = document.getElementById('modal-content');
    if (!overlay || !content) return;

    var lang = currentLang;
    var data = entry[lang] || entry['en'];
    var langIdx = { en: 0, ar: 1, zh: 2 }[lang] || 0;

    var specsHtml = data.specs.map(function (row) {
      var labelEntry = specLabels[row[0]];
      var label = labelEntry ? labelEntry[langIdx] : row[0];
      return '<tr><th>' + label + '</th><td>' + row[1] + '</td></tr>';
    }).join('');

    var btnLabel = inquireLabel[lang] || inquireLabel['en'];

    content.innerHTML =
      '<img src="' + entry.img + '" alt="' + data.title + '" loading="lazy">' +
      '<h2>' + data.title + '</h2>' +
      '<p>' + data.desc + '</p>' +
      (data.specs.length ? '<table><tbody>' + specsHtml + '</tbody></table>' : '') +
      '<div style="margin-top:24px;"><a href="#inquiry" class="baer-btn-v2" onclick="closeProductModal()" style="text-decoration:none;">' + btnLabel + '</a></div>';

    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.closeProductModal = function () {
    var overlay = document.getElementById('product-modal');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
  };

  document.addEventListener('click', function (e) {
    var overlay = document.getElementById('product-modal');
    if (overlay && e.target === overlay) {
      window.closeProductModal();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') window.closeProductModal();
  });

  /* ── i18n (language switcher) ── */
  var i18n = {
    en: {
      'nav-home': 'Home', 'nav-products': 'Products', 'nav-about': 'About Us',
      'nav-catalog': 'Catalog', 'nav-contact': 'Contact', 'nav-lang': 'LANGUAGE',
      'nav-quick-links': 'QUICK LINKS', 'nav-quote': 'Get a Quote',
      'h-t2': 'Modern Living Standards',
      'h-title2': 'PREMIUM <span>EXHAUST FAN</span><br>SERIES',
      'h-d2': 'Sleek designs with intelligent humidity sensors, delivering 26dB whisper-quiet performance for modern interiors.',
      'hero-view': 'VIEW RANGE',
      'series-01': '01. Exhaust Fan Series', 'series-02': '02. Mixed Flow Inline Duct Fans',
      'series-03': '03. Ventilation & Bathroom', 'series-04': '04. Silent Cabinet Fans',
      'view-specs': 'VIEW SPECS', 'view-details': 'DETAILS',
      'p01-title1': 'Ceiling Mount Exhaust Fan', 'p02-n1': 'Standard Window Fan',
      'p01-n3': 'Double-Grill Window Fan', 'p04-n1': 'Industrial Axial Fan',
      'p05-n1': 'Standard Mixed Flow Series', 'p02-n2': 'High-Efficiency Booster',
      'p02-n3': 'Intelligent DC Inverter', 'p03-n-last': 'Export Pro Bathroom Series',
      'p03-n2': 'Circular Pull-Cord Fan', 'p03-d2': 'Classic circular design with convenient pull-cord switch.',
      'p10-n1': 'Acoustic Cabinet Series', 'p13-n1': 'Fresh Air Purification Unit',
      'f-title': 'Industry Leading Manufacturing',
      'f-desc': 'Zhejiang Baer Electrical Technology Co., Ltd. is a professional ventilation supplier in Shengzhou, China.',
      'ws-1': 'RAW MATERIAL & MOLDS', 'ws-2': 'INJECTION MOLDING LINE', 'ws-3': 'CNC LASER CUTTING',
      'ws-4': 'PRODUCT ASSEMBLY', 'ws-5': 'MOTOR TESTING', 'ws-6': 'SAMPLE SHOWROOM',
      'ws-7': 'PROFESSIONAL PACKAGING', 'ws-8': 'GLOBAL WAREHOUSE',
      'inq-name': 'NAME', 'inq-email': 'EMAIL', 'inq-wa': 'WHATSAPP / MOBILE',
      'inq-type': 'PRODUCT TYPE', 'inq-req': 'DETAILED REQUIREMENTS', 'inq-submit': 'Submit Inquiry'
    },
    ar: {
      'nav-home': 'الرئيسية', 'nav-products': 'المنتجات', 'nav-about': 'من نحن',
      'nav-catalog': 'الكتالوج', 'nav-contact': 'اتصل بنا', 'nav-lang': 'اللغة',
      'nav-quick-links': 'روابط سريعة', 'nav-quote': 'طلب عرض سعر',
      'h-t2': 'معايير المعيشة العصرية',
      'h-title2': 'سلسلة <span>مراوح الشفط</span><br>الممتازة',
      'h-d2': 'تصميمات أنيقة مع مستشعرات الرطوبة الذكية، أداء هادئ 26dB للمساحات الداخلية الحديثة.',
      'hero-view': 'استعرض المنتجات',
      'series-01': '01. سلسلة مراوح الشفط', 'series-02': '02. مراوح القنوات المختلطة',
      'series-03': '03. تهوية الحمامات', 'series-04': '04. مراوح صامتة',
      'view-specs': 'المواصفات', 'view-details': 'التفاصيل',
      'p01-title1': 'مروحة شفط سقفية', 'p02-n1': 'مروحة نافذة قياسية',
      'p01-n3': 'مروحة نافذة مزدوجة الشبك', 'p04-n1': 'مروحة محورية صناعية',
      'p05-n1': 'سلسلة التدفق المختلط القياسي', 'p02-n2': 'معزز عالي الكفاءة',
      'p02-n3': 'عاكس DC الذكي', 'p03-n-last': 'سلسلة حمامات التصدير الاحترافية',
      'p03-n2': 'مروحة دائرية بسلسلة سحب', 'p03-d2': 'تصميم دائري كلاسيكي مع مفتاح سحب مريح.',
      'p10-n1': 'سلسلة خزانة صوتية', 'p13-n1': 'وحدة تنقية الهواء النقي',
      'f-title': 'تصنيع رائد في الصناعة',
      'f-desc': 'شركة Zhejiang Baer للتكنولوجيا الكهربائية، موردة تهوية احترافية في شنغتشو، الصين.',
      'ws-1': 'المواد الخام والقوالب', 'ws-2': 'خط حقن البلاستيك', 'ws-3': 'القطع بالليزر',
      'ws-4': 'تجميع المنتجات', 'ws-5': 'اختبار المحرك', 'ws-6': 'عرض النماذج',
      'ws-7': 'تغليف احترافي', 'ws-8': 'مستودع عالمي',
      'inq-name': 'الاسم', 'inq-email': 'البريد الإلكتروني', 'inq-wa': 'واتساب / موبايل',
      'inq-type': 'نوع المنتج', 'inq-req': 'المتطلبات التفصيلية', 'inq-submit': 'إرسال الاستفسار'
    },
    zh: {
      'nav-home': '首页', 'nav-products': '产品', 'nav-about': '关于我们',
      'nav-catalog': '产品目录', 'nav-contact': '联系我们', 'nav-lang': '语言',
      'nav-quick-links': '快速链接', 'nav-quote': '获取报价',
      'h-t2': '现代居住标准',
      'h-title2': '高端<span>换气扇</span><br>系列',
      'h-d2': '智能湿度传感器，26dB超静音设计，专为现代室内空间打造。',
      'hero-view': '查看系列',
      'series-01': '01. 换气扇系列', 'series-02': '02. 斜流管道风机',
      'series-03': '03. 卫浴通风', 'series-04': '04. 静音风机',
      'view-specs': '查看规格', 'view-details': '详情',
      'p01-title1': '吸顶换气扇', 'p02-n1': '标准窗式换气扇',
      'p01-n3': '双格栅窗式换气扇', 'p04-n1': '工业轴流风机',
      'p05-n1': '标准斜流系列', 'p02-n2': '高效助推风机',
      'p02-n3': '智能直流变频风机', 'p03-n-last': '出口卫浴系列',
      'p03-n2': '圆型拉绳换气扇', 'p03-d2': '经典圆形设计，便捷拉绳开关。',
      'p10-n1': '静音机柜系列', 'p13-n1': '新风净化机组',
      'f-title': '行业领先的制造实力',
      'f-desc': '浙江拜尔电气科技有限公司，中国嵊州专业通风设备供应商。',
      'ws-1': '原材料与模具', 'ws-2': '注塑成型线', 'ws-3': 'CNC激光切割',
      'ws-4': '产品装配', 'ws-5': '电机测试', 'ws-6': '样品展厅',
      'ws-7': '专业包装', 'ws-8': '全球仓储',
      'inq-name': '姓名', 'inq-email': '邮箱', 'inq-wa': 'WhatsApp / 手机',
      'inq-type': '产品类型', 'inq-req': '详细需求', 'inq-submit': '提交询盘'
    }
  };

  window.setLanguage = function (lang) {
    if (!i18n[lang]) return;
    currentLang = lang;
    var dict = i18n[lang];
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      if (dict[key] !== undefined) el.innerHTML = dict[key];
    });
    document.documentElement.lang = lang;
    document.documentElement.dir  = lang === 'ar' ? 'rtl' : 'ltr';
    langContent && langContent.classList.remove('open');
    try { localStorage.setItem('baer-lang', lang); } catch (e) {}
  };

  /* restore saved language */
  try {
    var saved = localStorage.getItem('baer-lang');
    if (saved && i18n[saved]) { currentLang = saved; window.setLanguage(saved); }
  } catch (e) {}

})();
