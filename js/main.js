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

    'Size':            ['Size',            'المقاس',           '尺寸',     'mm'],

    'Airflow':         ['Airflow',         'تدفق الهواء',      '风量',     'm³/h'],

    'Noise':           ['Noise',           'مستوى الضوضاء',    '噪音',     'dB(A)'],

    'Power':           ['Power',           'الطاقة',           '功率',     'W'],

    'Voltage':         ['Voltage',         'الجهد الكهربائي',  '电压',     'V/Hz'],

    'Certification':   ['Certification',   'الشهادات',         '认证',     ''],

    'Static Pressure': ['Static Pressure', 'الضغط الستاتيكي',  '静压',     'Pa'],

    'IP Rating':       ['IP Rating',       'IP',               'IP防护等级','IP'],

    'Motor':           ['Motor',           'المحرك',           '电机',     ''],

    'Energy Saving':   ['Energy Saving',   'توفير الطاقة',     '节能',     ''],

    'Control':         ['Control',         'التحكم',           '控制方式', ''],

    'Filter':          ['Filter',          'الفلتر',           '过滤器',   ''],

    'Heat Recovery':   ['Heat Recovery',   'استعادة الحرارة',  '热回收效率',''],

    'Application':     ['Application',     'التطبيقات',        '应用场景', ''],

    'Switch':          ['Switch',          'مفتاح التشغيل',    '开关方式', ''],

    'MOQ':             ['MOQ',             'الحد الأدنى للطلب','最小起订量','pcs']

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

            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Panel Size</th><th>Install Size</th><th>Outlet</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Speed</th><th>Noise</th><th>Pcs/Ctn</th><th>CBM</th><th>G.W.</th><th>N.W.</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th><th class="unit">(pcs)</th><th class="unit">(m³)</th><th class="unit">(Kg/Ctn)</th><th class="unit">(Kg/Ctn)</th></tr><tr><td>KLT-10B 6"</td><td>200×200</td><td>160×160</td><td>Φ85</td><td>220/50</td><td>30 W</td><td>150 m³/h</td><td>1200 r/min</td><td>35 dB</td><td>20 pcs/ctn</td><td>0.11 m³</td><td>20 kg</td><td>19 kg</td></tr><tr><td>KLT-12B 8"</td><td>250×250</td><td>205×205</td><td>Φ100</td><td>220/50</td><td>30 W</td><td>380 m³/h</td><td>1200 r/min</td><td>38 dB</td><td>9 pcs/ctn</td><td>0.119 m³</td><td>12.8 kg</td><td>11.8 kg</td></tr><tr><td>KLT-16B 9"</td><td>280×280</td><td>225×225</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>396 m³/h</td><td>1100 r/min</td><td>40 dB</td><td>9 pcs/ctn</td><td>0.15 m³</td><td>15.6 kg</td><td>14.6 kg</td></tr><tr><td>KLT-18B 10"</td><td>310×310</td><td>245×245</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>432 m³/h</td><td>1130 r/min</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.168 m³</td><td>17.5 kg</td><td>16.5 kg</td></tr><tr><td>KLT-20B 12"</td><td>340×340</td><td>290×290</td><td>Φ100</td><td>220/50</td><td>80 W</td><td>792 m³/h</td><td>1100 r/min</td><td>45 dB</td><td>6 pcs/ctn</td><td>0.145 m³</td><td>15.3 kg</td><td>14.3 kg</td></tr><tr><td>KLT-25B 14"</td><td>400×400</td><td>330×330</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1500 m³/h</td><td>650 r/min</td><td>48 dB</td><td>4 pcs/ctn</td><td>0.146 m³</td><td>13.5 kg</td><td>12.8 kg</td></tr><tr><td>KLT-30B 18"</td><td>600×600</td><td>480×480</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1800 m³/h</td><td>685 r/min</td><td>48 dB</td><td>1 pcs/ctn</td><td>0.109 m³</td><td>6.3 kg</td><td>5.7 kg</td></tr></table>' },

      ar: { title: 'مروحة شفط سقفية',

            desc:  'مروحة شفط سقفية موفرة للطاقة مصممة للاستخدامات السكنية والتجارية الخفيفة. تتميز بمحرك منخفض الضوضاء وغالق تلقائي وتركيب شبكي سهل.',

            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>حجم اللوحة</th><th>حجم التركيب</th><th>المخرج</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>السرعة</th><th>الضوضاء</th><th>قطعة/كرتون</th><th>حجم الكرتون</th><th>الوزن القائم</th><th>الوزن الصافي</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th><th class="unit">(قطعة)</th><th class="unit">(m³)</th><th class="unit">(Kg/كرتون)</th><th class="unit">(Kg/كرتون)</th></tr><tr><td>KLT-10B 6"</td><td>200×200</td><td>160×160</td><td>Φ85</td><td>220/50</td><td>30 W</td><td>150 m³/h</td><td>1200 r/min</td><td>35 dB</td><td>20 pcs/ctn</td><td>0.11 m³</td><td>20 kg</td><td>19 kg</td></tr><tr><td>KLT-12B 8"</td><td>250×250</td><td>205×205</td><td>Φ100</td><td>220/50</td><td>30 W</td><td>380 m³/h</td><td>1200 r/min</td><td>38 dB</td><td>9 pcs/ctn</td><td>0.119 m³</td><td>12.8 kg</td><td>11.8 kg</td></tr><tr><td>KLT-16B 9"</td><td>280×280</td><td>225×225</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>396 m³/h</td><td>1100 r/min</td><td>40 dB</td><td>9 pcs/ctn</td><td>0.15 m³</td><td>15.6 kg</td><td>14.6 kg</td></tr><tr><td>KLT-18B 10"</td><td>310×310</td><td>245×245</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>432 m³/h</td><td>1130 r/min</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.168 m³</td><td>17.5 kg</td><td>16.5 kg</td></tr><tr><td>KLT-20B 12"</td><td>340×340</td><td>290×290</td><td>Φ100</td><td>220/50</td><td>80 W</td><td>792 m³/h</td><td>1100 r/min</td><td>45 dB</td><td>6 pcs/ctn</td><td>0.145 m³</td><td>15.3 kg</td><td>14.3 kg</td></tr><tr><td>KLT-25B 14"</td><td>400×400</td><td>330×330</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1500 m³/h</td><td>650 r/min</td><td>48 dB</td><td>4 pcs/ctn</td><td>0.146 m³</td><td>13.5 kg</td><td>12.8 kg</td></tr><tr><td>KLT-30B 18"</td><td>600×600</td><td>480×480</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1800 m³/h</td><td>685 r/min</td><td>48 dB</td><td>1 pcs/ctn</td><td>0.109 m³</td><td>6.3 kg</td><td>5.7 kg</td></tr></table>' },

      zh: { title: '吸顶换气扇',

            desc:  '节能吸顶式换气扇，专为住宅及轻商业场所设计。具备低噪音电机、自动百叶和简易格栅安装功能。',

            specs: [['Size','100mm / 150mm / 200mm'],['Airflow','80~350 m³/h'],['Noise','≤26 dB(A)'],['Power','8~25 W'],['Voltage','220V / 50Hz'],['Certification','CE, RoHS']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>面板尺寸</th><th>开孔尺寸</th><th>出风口</th><th>电压</th><th>功率</th><th>风量</th><th>转速</th><th>噪音</th><th>装箱数</th><th>单箱体积</th><th>毛重</th><th>净重</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th><th class="unit">(件)</th><th class="unit">(m³)</th><th class="unit">(Kg/箱)</th><th class="unit">(Kg/箱)</th></tr><tr><td>KLT-10B 6"</td><td>200×200</td><td>160×160</td><td>Φ85</td><td>220/50</td><td>30 W</td><td>150 m³/h</td><td>1200 r/min</td><td>35 dB</td><td>20 pcs/ctn</td><td>0.11 m³</td><td>20 kg</td><td>19 kg</td></tr><tr><td>KLT-12B 8"</td><td>250×250</td><td>205×205</td><td>Φ100</td><td>220/50</td><td>30 W</td><td>380 m³/h</td><td>1200 r/min</td><td>38 dB</td><td>9 pcs/ctn</td><td>0.119 m³</td><td>12.8 kg</td><td>11.8 kg</td></tr><tr><td>KLT-16B 9"</td><td>280×280</td><td>225×225</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>396 m³/h</td><td>1100 r/min</td><td>40 dB</td><td>9 pcs/ctn</td><td>0.15 m³</td><td>15.6 kg</td><td>14.6 kg</td></tr><tr><td>KLT-18B 10"</td><td>310×310</td><td>245×245</td><td>Φ100</td><td>220/50</td><td>40 W</td><td>432 m³/h</td><td>1130 r/min</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.168 m³</td><td>17.5 kg</td><td>16.5 kg</td></tr><tr><td>KLT-20B 12"</td><td>340×340</td><td>290×290</td><td>Φ100</td><td>220/50</td><td>80 W</td><td>792 m³/h</td><td>1100 r/min</td><td>45 dB</td><td>6 pcs/ctn</td><td>0.145 m³</td><td>15.3 kg</td><td>14.3 kg</td></tr><tr><td>KLT-25B 14"</td><td>400×400</td><td>330×330</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1500 m³/h</td><td>650 r/min</td><td>48 dB</td><td>4 pcs/ctn</td><td>0.146 m³</td><td>13.5 kg</td><td>12.8 kg</td></tr><tr><td>KLT-30B 18"</td><td>600×600</td><td>480×480</td><td>Φ150</td><td>220/50</td><td>120 W</td><td>1800 m³/h</td><td>685 r/min</td><td>48 dB</td><td>1 pcs/ctn</td><td>0.109 m³</td><td>6.3 kg</td><td>5.7 kg</td></tr></table>' }

    },

    p2: {

      img: 'https://sc02.alicdn.com/kf/H5fbe6fbc92284181968eba3dff7ed880E.jpg',

      en: { title: 'Standard Window Fan',

            desc:  'Classic window-mounted exhaust fan suitable for kitchens, bathrooms, and small workshops. Durable ABS housing with anti-back-draft shutter.',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Panel Size</th><th>Install Size</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Noise</th><th>Pcs/Ctn</th><th>CBM</th><th>G.W.</th><th>N.W.</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(pcs)</th><th class="unit">(m³)</th><th class="unit">(kg)</th><th class="unit">(kg)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' },

      ar: { title: 'مروحة نافذة قياسية',

            desc:  'مروحة شفط كلاسيكية مثبتة على النافذة مناسبة للمطابخ والحمامات والورش الصغيرة. هيكل ABS متين مع غالق مضاد للتدفق العكسي.',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>حجم اللوحة</th><th>حجم التركيب</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>الضوضاء</th><th>قطعة/كرتون</th><th>حجم الكرتون</th><th>الوزن القائم</th><th>الوزن الصافي</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(pcs)</th><th class="unit">(m³)</th><th class="unit">(kg)</th><th class="unit">(kg)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' },

      zh: { title: '标准窗式换气扇',

            desc:  '经典窗式安装换气扇，适用于厨房、卫浴及小型工作间。耐用ABS外壳，配备防回流百叶。',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','120~450 m³/h'],['Noise','≤38 dB(A)'],['Power','15~45 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>面板尺寸</th><th>安装尺寸</th><th>电压</th><th>功率</th><th>风量</th><th>噪音</th><th>装箱数</th><th>单箱体积</th><th>毛重</th><th>净重</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(件)</th><th class="unit">(m³)</th><th class="unit">(Kg/箱)</th><th class="unit">(Kg/箱)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' }

    },

    p3: {

      img: 'https://sc02.alicdn.com/kf/A216d65f6e04a43438a882ca3e9b88721Z.png',

      en: { title: 'Double-Grill Window Fan',

            desc:  'Two-layer grille design for improved airflow direction control. Ideal for through-wall installation in residential and commercial buildings.',

            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Panel Size</th><th>Install Size</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Noise</th><th>Pcs/Ctn</th><th>CBM</th><th>G.W.</th><th>N.W.</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(pcs)</th><th class="unit">(m³)</th><th class="unit">(kg)</th><th class="unit">(kg)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' },

      ar: { title: 'مروحة نافذة مزدوجة الشبك',

            desc:  'تصميم شبكي مزدوج لتحسين التحكم في اتجاه تدفق الهواء. مثالية للتركيب في الجدران للمباني السكنية والتجارية.',

            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>حجم اللوحة</th><th>حجم التركيب</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>الضوضاء</th><th>قطعة/كرتون</th><th>حجم الكرتون</th><th>الوزن القائم</th><th>الوزن الصافي</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(pcs)</th><th class="unit">(m³)</th><th class="unit">(kg)</th><th class="unit">(kg)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' },

      zh: { title: '双格栅窗式换气扇',

            desc:  '双层格栅设计，有效改善气流方向控制。适合住宅及商业建筑穿墙安装。',

            specs: [['Size','150mm / 200mm'],['Airflow','140~380 m³/h'],['Noise','≤32 dB(A)'],['Power','18~35 W'],['Voltage','220V / 50Hz']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>面板尺寸</th><th>安装尺寸</th><th>电压</th><th>功率</th><th>风量</th><th>噪音</th><th>装箱数</th><th>单箱体积</th><th>毛重</th><th>净重</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(dB)</th><th class="unit">(件)</th><th class="unit">(m³)</th><th class="unit">(Kg/箱)</th><th class="unit">(Kg/箱)</th></tr><tr><td>KLT-20B 8"</td><td>300×300</td><td>245×245</td><td>220/50</td><td>40 W</td><td>468 m³/h</td><td>38 dB</td><td>8 pcs/ctn</td><td>0.116 m³</td><td>14.3 kg</td><td>13 kg</td></tr><tr><td>KLT-25B 10"</td><td>335×335</td><td>280×280</td><td>220/50</td><td>40 W</td><td>792 m³/h</td><td>42 dB</td><td>8 pcs/ctn</td><td>0.149 m³</td><td>16.9 kg</td><td>15.4 kg</td></tr><tr><td>KLT-30B 12"</td><td>380×380</td><td>325×325</td><td>220/50</td><td>40 W</td><td>984 m³/h</td><td>45 dB</td><td>5 pcs/ctn</td><td>0.122 m³</td><td>13.8 kg</td><td>12.8 kg</td></tr></table>' }

    },

    p4: {

      img: 'https://sc02.alicdn.com/kf/H42e66ea71d5445fcbb62c7c68e493d94v.jpg',

      en: { title: 'Industrial Axial Fan',

            desc:  'Heavy-duty axial fan for industrial ventilation. High static pressure, continuous duty, IP55 rated for harsh environments.',

            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Size</th><th>Voltage</th><th>Power</th><th>Speed</th><th>Airflow</th><th>Noise</th></tr><tr><th class="unit">(inch)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(r/min)</th><th class="unit">(CFM)</th><th class="unit">(dB)</th></tr><tr><td>FA8-20 8"</td><td>200 mm</td><td>220/50</td><td>20 W</td><td>1400 r/min</td><td>360 CFM</td><td>46 dB</td></tr><tr><td>FA10-25 10"</td><td>250 mm</td><td>220/50</td><td>30 W</td><td>1400 r/min</td><td>540 CFM</td><td>50 dB</td></tr><tr><td>FA12-30 12"</td><td>300 mm</td><td>220/50</td><td>45 W</td><td>1400 r/min</td><td>760 CFM</td><td>55 dB</td></tr><tr><td>FA14-35 14"</td><td>350 mm</td><td>220/50</td><td>100 W</td><td>1400 r/min</td><td>1650 CFM</td><td>60 dB</td></tr><tr><td>FA16-40 16"</td><td>400 mm</td><td>220/50</td><td>150 W</td><td>1400 r/min</td><td>2000 CFM</td><td>68 dB</td></tr></table>' },

      ar: { title: 'مروحة محورية صناعية',

            desc:  'مروحة محورية للأعمال الشاقة للتهوية الصناعية. ضغط ستاتيكي عالٍ، تشغيل مستمر، مقاومة IP55 للبيئات القاسية.',

            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>الحجم</th><th>الجهد</th><th>القدرة</th><th>السرعة</th><th>تدفق الهواء</th><th>الضوضاء</th></tr><tr><th class="unit">(inch)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(r/min)</th><th class="unit">(CFM)</th><th class="unit">(dB)</th></tr><tr><td>FA8-20 8"</td><td>200 mm</td><td>220/50</td><td>20 W</td><td>1400 r/min</td><td>360 CFM</td><td>46 dB</td></tr><tr><td>FA10-25 10"</td><td>250 mm</td><td>220/50</td><td>30 W</td><td>1400 r/min</td><td>540 CFM</td><td>50 dB</td></tr><tr><td>FA12-30 12"</td><td>300 mm</td><td>220/50</td><td>45 W</td><td>1400 r/min</td><td>760 CFM</td><td>55 dB</td></tr><tr><td>FA14-35 14"</td><td>350 mm</td><td>220/50</td><td>100 W</td><td>1400 r/min</td><td>1650 CFM</td><td>60 dB</td></tr><tr><td>FA16-40 16"</td><td>400 mm</td><td>220/50</td><td>150 W</td><td>1400 r/min</td><td>2000 CFM</td><td>68 dB</td></tr></table>' },

      zh: { title: '工业轴流风机',

            desc:  '重型轴流风机，适用于工业通风场合。高静压，可连续运行，IP55防护等级，耐恶劣环境。',

            specs: [['Size','300mm ~ 800mm'],['Airflow','1000~25000 m³/h'],['Static Pressure','Up to 180 Pa'],['Power','0.25~5.5 kW'],['IP Rating','IP55']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>尺寸</th><th>电压</th><th>功率</th><th>转速</th><th>风量</th><th>噪音</th></tr><tr><th class="unit">(英寸)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(r/min)</th><th class="unit">(CFM)</th><th class="unit">(dB)</th></tr><tr><td>FA8-20 8"</td><td>200 mm</td><td>220/50</td><td>20 W</td><td>1400 r/min</td><td>360 CFM</td><td>46 dB</td></tr><tr><td>FA10-25 10"</td><td>250 mm</td><td>220/50</td><td>30 W</td><td>1400 r/min</td><td>540 CFM</td><td>50 dB</td></tr><tr><td>FA12-30 12"</td><td>300 mm</td><td>220/50</td><td>45 W</td><td>1400 r/min</td><td>760 CFM</td><td>55 dB</td></tr><tr><td>FA14-35 14"</td><td>350 mm</td><td>220/50</td><td>100 W</td><td>1400 r/min</td><td>1650 CFM</td><td>60 dB</td></tr><tr><td>FA16-40 16"</td><td>400 mm</td><td>220/50</td><td>150 W</td><td>1400 r/min</td><td>2000 CFM</td><td>68 dB</td></tr></table>' }

    },

    p5: {

      img: 'https://sc02.alicdn.com/kf/Hf77c8f2216ff4576b9f83c896fdd000fq.jpg',

      en: { title: 'Standard Mixed Flow Series',

            desc:  'Inline duct fan combining axial and centrifugal design for high airflow with moderate static pressure. Suitable for residential HRV and HVAC duct systems.',

            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Size</th><th>Outlet Size</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Wind Pressure</th><th>Speed</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4-inch 2C Single Speed</td><td>303×176×203</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>5-inch 2C Single Speed</td><td>303×176×203</td><td>Φ125</td><td>50 W</td><td>420 m³/h</td><td>180 pa</td><td>2650 r/min</td></tr><tr><td>6-inch 2C Single Speed</td><td>320×200×227</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8-inch 2C Single Speed</td><td>320×217×305</td><td>Φ200</td><td>120 W</td><td>1200 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>10-inch 2C Single Speed</td><td>305×295×385</td><td>Φ250</td><td>200 W</td><td>1800 m³/h</td><td>488 pa</td><td>2000 r/min</td></tr><tr><td>12-inch 2C Single Speed</td><td>340×310×445</td><td>Φ315</td><td>330 W</td><td>2200 m³/h</td><td>693 pa</td><td>1650 r/min</td></tr><tr><td>4-inch 2C Two Speed</td><td>303×176×203</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>5-inch 2C Two Speed</td><td>303×176×203</td><td>Φ125</td><td>H:56 L:50</td><td>H:420 L:330</td><td>H:180 L:120</td><td>H:2650 L:2100</td></tr><tr><td>6-inch 2C Two Speed</td><td>320×200×227</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8-inch 2C Two Speed</td><td>320×217×305</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr><tr><td>10-inch 2C Two Speed</td><td>305×295×385</td><td>Φ250</td><td>H:200 L:160</td><td>H:1800 L:1400</td><td>H:488 L:371</td><td>H:2000 L:1600</td></tr><tr><td>12-inch 2C Two Speed</td><td>340×310×445</td><td>Φ315</td><td>H:330 L:200</td><td>H:2200 L:1750</td><td>H:693 L:435</td><td>H:2350 L:1650</td></tr></table>' },

      ar: { title: 'سلسلة التدفق المختلط القياسي',

            desc:  'مروحة قناة مدمجة تجمع بين التصميم المحوري والطرد المركزي لتدفق هواء عالٍ مع ضغط ستاتيكي معتدل. مناسبة لأنظمة HRV السكنية وقنوات HVAC.',

            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>الحجم</th><th>حجم المخرج</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>ضغط الهواء</th><th>السرعة</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4 بوصة 2C سرعة واحدة</td><td>303×176×203</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>5 بوصة 2C سرعة واحدة</td><td>303×176×203</td><td>Φ125</td><td>50 W</td><td>420 m³/h</td><td>180 pa</td><td>2650 r/min</td></tr><tr><td>6 بوصة 2C سرعة واحدة</td><td>320×200×227</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8 بوصة 2C سرعة واحدة</td><td>320×217×305</td><td>Φ200</td><td>120 W</td><td>1200 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>10 بوصة 2C سرعة واحدة</td><td>305×295×385</td><td>Φ250</td><td>200 W</td><td>1800 m³/h</td><td>488 pa</td><td>2000 r/min</td></tr><tr><td>12 بوصة 2C سرعة واحدة</td><td>340×310×445</td><td>Φ315</td><td>330 W</td><td>2200 m³/h</td><td>693 pa</td><td>1650 r/min</td></tr><tr><td>4 بوصة 2C سرعتان</td><td>303×176×203</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>5 بوصة 2C سرعتان</td><td>303×176×203</td><td>Φ125</td><td>H:56 L:50</td><td>H:420 L:330</td><td>H:180 L:120</td><td>H:2650 L:2100</td></tr><tr><td>6 بوصة 2C سرعتان</td><td>320×200×227</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8 بوصة 2C سرعتان</td><td>320×217×305</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr><tr><td>10 بوصة 2C سرعتان</td><td>305×295×385</td><td>Φ250</td><td>H:200 L:160</td><td>H:1800 L:1400</td><td>H:488 L:371</td><td>H:2000 L:1600</td></tr><tr><td>12 بوصة 2C سرعتان</td><td>340×310×445</td><td>Φ315</td><td>H:330 L:200</td><td>H:2200 L:1750</td><td>H:693 L:435</td><td>H:2350 L:1650</td></tr></table>' },

      zh: { title: '标准斜流管道风机',

            desc:  '管道内嵌式风机，融合轴流与离心设计，高风量、中等静压。适用于住宅新风系统及暖通管道。',

            specs: [['Size','100mm / 125mm / 150mm / 200mm'],['Airflow','100~800 m³/h'],['Static Pressure','Up to 180 Pa'],['Noise','≤38 dB(A)'],['Power','25~110 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>尺寸</th><th>出风口</th><th>电压</th><th>功率</th><th>风量</th><th>风压</th><th>转速</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4寸 2C 单速</td><td>303×176×203</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>5寸 2C 单速</td><td>303×176×203</td><td>Φ125</td><td>50 W</td><td>420 m³/h</td><td>180 pa</td><td>2650 r/min</td></tr><tr><td>6寸 2C 单速</td><td>320×200×227</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8寸 2C 单速</td><td>320×217×305</td><td>Φ200</td><td>120 W</td><td>1200 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>10寸 2C 单速</td><td>305×295×385</td><td>Φ250</td><td>200 W</td><td>1800 m³/h</td><td>488 pa</td><td>2000 r/min</td></tr><tr><td>12寸 2C 单速</td><td>340×310×445</td><td>Φ315</td><td>330 W</td><td>2200 m³/h</td><td>693 pa</td><td>1650 r/min</td></tr><tr><td>4寸 2C 双速</td><td>303×176×203</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>5寸 2C 双速</td><td>303×176×203</td><td>Φ125</td><td>H:56 L:50</td><td>H:420 L:330</td><td>H:180 L:120</td><td>H:2650 L:2100</td></tr><tr><td>6寸 2C 双速</td><td>320×200×227</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8寸 2C 双速</td><td>320×217×305</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr><tr><td>10寸 2C 双速</td><td>305×295×385</td><td>Φ250</td><td>H:200 L:160</td><td>H:1800 L:1400</td><td>H:488 L:371</td><td>H:2000 L:1600</td></tr><tr><td>12寸 2C 双速</td><td>340×310×445</td><td>Φ315</td><td>H:330 L:200</td><td>H:2200 L:1750</td><td>H:693 L:435</td><td>H:2350 L:1650</td></tr></table>' }

    },

    p7: {

      img: 'https://sc02.alicdn.com/kf/A69a6450d8e504c9a9c1dcaedccad5c3e2.png',

      en: { title: 'High-Efficiency Booster Fan',

            desc:  'Mixed flow booster for long duct runs. High static pressure overcomes resistance in complex HVAC systems.',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Size</th><th>Outlet Size</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Wind Pressure</th><th>Speed</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4-inch Booster Single Speed</td><td>360×205×180</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>6-inch Booster Single Speed</td><td>365×235×200</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8-inch Booster Single Speed</td><td>385×255×225</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>4-inch Booster Two Speed</td><td>360×205×180</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>6-inch Booster Two Speed</td><td>365×235×200</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8-inch Booster Two Speed</td><td>385×255×225</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr></table>' },

      ar: { title: 'معزز تدفق عالي الكفاءة',

            desc:  'معزز تدفق مختلط لمسارات القنوات الطويلة. ضغط ستاتيكي عالٍ يتغلب على مقاومة أنظمة HVAC المعقدة.',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>الحجم</th><th>حجم المخرج</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>ضغط الهواء</th><th>السرعة</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4 بوصة معزز سرعة واحدة</td><td>360×205×180</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>6 بوصة معزز سرعة واحدة</td><td>365×235×200</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8 بوصة معزز سرعة واحدة</td><td>385×255×225</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>4 بوصة معزز سرعتان</td><td>360×205×180</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>6 بوصة معزز سرعتان</td><td>365×235×200</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8 بوصة معزز سرعتان</td><td>385×255×225</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr></table>' },

      zh: { title: '高效助推风机',

            desc:  '斜流助推风机，适用于长管道场合。超高静压，克服复杂暖通系统阻力。',

            specs: [['Size','150mm / 200mm / 250mm'],['Airflow','300~1200 m³/h'],['Static Pressure','Up to 280 Pa'],['Power','55~250 W']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>尺寸</th><th>出风口</th><th>电压</th><th>功率</th><th>风量</th><th>风压</th><th>转速</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th></tr><tr><td>4寸 助推风机 单速</td><td>360×205×180</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td></tr><tr><td>6寸 助推风机 单速</td><td>365×235×200</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td></tr><tr><td>8寸 助推风机 单速</td><td>385×255×225</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>380 pa</td><td>2100 r/min</td></tr><tr><td>4寸 助推风机 双速</td><td>360×205×180</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:110</td><td>H:2750 L:2450</td></tr><tr><td>6寸 助推风机 双速</td><td>365×235×200</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:245</td><td>H:2450 L:2000</td></tr><tr><td>8寸 助推风机 双速</td><td>385×255×225</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:380 L:274</td><td>H:2100 L:1950</td></tr></table>' }

    },

    p8: {

      img: 'https://sc02.alicdn.com/kf/A96cb71eed6d94b289be81e750dfc9fe1M.png',

      en: { title: 'Intelligent DC Inverter Fan',

            desc:  'DC brushless motor with variable speed control. Up to 60% energy saving vs AC equivalents. Smart humidity / CO₂ trigger available.',

            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','DC Brushless'],['Energy Saving','Up to 60%'],['Control','PWM / 0-10V / Smart Sensor']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">Model</th><th>Size</th><th>Outlet Size</th><th>Voltage</th><th>Power</th><th>Airflow</th><th>Wind Pressure</th><th>Speed</th><th>Noise</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th></tr><tr><td>4-inch DC Single Speed</td><td>450×200×215</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td><td>30 dB</td></tr><tr><td>6-inch DC Single Speed</td><td>495×240×260</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td><td>35 dB</td></tr><tr><td>8-inch DC Single Speed</td><td>567×260×292</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>350 pa</td><td>2100 r/min</td><td>40 dB</td></tr><tr><td>4-inch DC Two Speed</td><td>450×200×215</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:125</td><td>H:2750 L:2450</td><td>30 dB</td></tr><tr><td>6-inch DC Two Speed</td><td>495×240×260</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:250</td><td>H:2450 L:2000</td><td>35 dB</td></tr><tr><td>8-inch DC Two Speed</td><td>567×260×292</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:360 L:280</td><td>H:2100 L:1950</td><td>40 dB</td></tr></table>' },

      ar: { title: 'مروحة عاكس DC الذكية',

            desc:  'محرك بدون فرش DC مع تحكم في السرعة المتغيرة. توفير طاقة يصل إلى 60% مقارنة بنظيراتها AC. متوفر مع مشغل رطوبة / CO₂ ذكي.',

            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','DC بدون فرش'],['Energy Saving','حتى 60%'],['Control','PWM / 0-10V / حساس ذكي']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">الموديل</th><th>الحجم</th><th>حجم المخرج</th><th>الجهد</th><th>القدرة</th><th>تدفق الهواء</th><th>ضغط الهواء</th><th>السرعة</th><th>الضوضاء</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th></tr><tr><td>4 بوصة DC سرعة واحدة</td><td>450×200×215</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td><td>30 dB</td></tr><tr><td>6 بوصة DC سرعة واحدة</td><td>495×240×260</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td><td>35 dB</td></tr><tr><td>8 بوصة DC سرعة واحدة</td><td>567×260×292</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>350 pa</td><td>2100 r/min</td><td>40 dB</td></tr><tr><td>4 بوصة DC سرعتان</td><td>450×200×215</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:125</td><td>H:2750 L:2450</td><td>30 dB</td></tr><tr><td>6 بوصة DC سرعتان</td><td>495×240×260</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:250</td><td>H:2450 L:2000</td><td>35 dB</td></tr><tr><td>8 بوصة DC سرعتان</td><td>567×260×292</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:360 L:280</td><td>H:2100 L:1950</td><td>40 dB</td></tr></table>' },

      zh: { title: '智能直流变频风机',

            desc:  '直流无刷电机，无级变速控制。比同规格交流产品节能最高60%。可选配湿度/CO₂智能触发。',

            specs: [['Size','125mm / 150mm / 200mm'],['Airflow','150~900 m³/h'],['Motor','直流无刷'],['Energy Saving','最高节能60%'],['Control','PWM / 0-10V / 智能传感器']],
            specTable: '<table class="spec-table"><tr><th rowspan="2">型号</th><th>尺寸</th><th>出风口</th><th>电压</th><th>功率</th><th>风量</th><th>风压</th><th>转速</th><th>噪音</th></tr><tr><th class="unit">(mm)</th><th class="unit">(mm)</th><th class="unit">(V/Hz)</th><th class="unit">(W)</th><th class="unit">(m³/h)</th><th class="unit">(pa)</th><th class="unit">(r/min)</th><th class="unit">(dB)</th></tr><tr><td>4寸 直流 单速</td><td>450×200×215</td><td>Φ100</td><td>48 W</td><td>290 m³/h</td><td>150 pa</td><td>2750 r/min</td><td>30 dB</td></tr><tr><td>6寸 直流 单速</td><td>495×240×260</td><td>Φ150</td><td>60 W</td><td>620 m³/h</td><td>300 pa</td><td>2450 r/min</td><td>35 dB</td></tr><tr><td>8寸 直流 单速</td><td>567×260×292</td><td>Φ200</td><td>120 W</td><td>1120 m³/h</td><td>350 pa</td><td>2100 r/min</td><td>40 dB</td></tr><tr><td>4寸 直流 双速</td><td>450×200×215</td><td>Φ100</td><td>H:48 L:42</td><td>H:330 L:280</td><td>H:150 L:125</td><td>H:2750 L:2450</td><td>30 dB</td></tr><tr><td>6寸 直流 双速</td><td>495×240×260</td><td>Φ150</td><td>H:60 L:50</td><td>H:600 L:480</td><td>H:300 L:250</td><td>H:2450 L:2000</td><td>35 dB</td></tr><tr><td>8寸 直流 双速</td><td>567×260×292</td><td>Φ200</td><td>H:120 L:90</td><td>H:1200 L:900</td><td>H:360 L:280</td><td>H:2100 L:1950</td><td>40 dB</td></tr></table>' }

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

      var unit = (labelEntry && labelEntry[3]) ? labelEntry[3] : '';

      var unitHtml = unit ? '<small class="baer-unit">(' + unit + ')</small>' : '';

      return '<tr><th>' + label + unitHtml + '</th><td>' + row[1] + '</td></tr>';

    }).join('');



    var btnLabel = inquireLabel[lang] || inquireLabel['en'];



    content.innerHTML =

      '<img src="' + entry.img + '" alt="' + data.title + '" loading="lazy">' +

      '<h2>' + data.title + '</h2>' +

      '<p>' + data.desc + '</p>' +

      (data.specTable ?

       '<div class="baer-modal-specwrap">' + data.specTable + '</div>' +

       '<style>.baer-modal-specwrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:4px 0;}.baer-modal-specwrap table.spec-table{border-collapse:collapse;width:100%;min-width:840px;font-size:12px;}.baer-modal-specwrap table.spec-table th,.baer-modal-specwrap table.spec-table td{border:1px solid #e2e6ec;padding:8px 10px;text-align:center;white-space:nowrap;}.baer-modal-specwrap table.spec-table th{background:#f4f6fa;font-weight:700;font-size:12px;}.baer-modal-specwrap table.spec-table th.unit{font-size:10px;font-weight:500;color:#888;text-transform:none;}.baer-modal-specwrap table.spec-table td:first-child{font-weight:700;background:#fafbfc;}</style>'

       : (data.specs.length ? '<table class="baer-modal-spec"><tbody>' + specsHtml + '</tbody></table>' +

       '<style>.baer-modal-spec th small.baer-unit{display:block;font-size:10px;font-weight:500;color:#888;margin-top:3px;text-transform:none;letter-spacing:0;}</style>' : '')) +

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

      'inq-type': 'PRODUCT TYPE', 'inq-req': 'DETAILED REQUIREMENTS', 'inq-submit': 'Submit Inquiry',

      'cert-tag': 'CERTIFIED & COMPLIANT', 'cert-title': 'International Quality Certifications',

      'cert-desc': 'Every BAER product is tested and certified to meet global safety and performance standards.',

      'cert-ce': 'EU Market Access', 'cert-3c': 'China Compulsory Cert.', 'cert-iso': 'Quality Management',

      'cert-cb': 'IEC Global Safety', 'cert-saa': 'Australia Approved', 'cert-etl': 'North America Listed',

      'cert-note': '* Certificates available upon request with every order',

      'app-tag': 'WHERE WE SERVE', 'app-title': 'Application Scenarios',

      'app-desc': 'BAER fans are deployed in residential, commercial and industrial settings across 50+ countries.',

      'app-1': 'Residential', 'app-1d': 'Bedroom · Kitchen · Bathroom',

      'app-2': 'Industrial', 'app-2d': 'Factory · Workshop · Warehouse',

      'app-3': 'Commercial', 'app-3d': 'Office · Mall · Hotel · Restaurant',

      'app-4': 'Healthcare', 'app-4d': 'Hospital · Clinic · Pharmacy',

      'app-5': 'HVAC Projects', 'app-5d': 'Fresh Air · Heat Recovery · IAQ',

      'why-tag': 'WHY BAER', 'why-title': 'Why Global Buyers Choose Us',

      'why-1h': 'Factory Direct', 'why-1d': '50,000m² own factory in Zhejiang. No middlemen — direct pricing means 15–30% lower cost vs trading companies.',

      'why-2h': 'OEM / ODM Capability', 'why-2d': 'Custom logo, color, voltage, blade design, and packaging. MOQ from 500 pcs. Full private-label solutions available.',

      'why-3h': 'Fast Lead Time', 'why-3d': 'Sample in 7 days. Mass production in 25–35 days. In-stock models ship within 3 days.',

      'why-4h': '2-Year Warranty', 'why-4d': 'All products carry a 2-year warranty. Defective units replaced or refunded within 30 days of confirmation.',

      'why-5h': 'CE / RoHS Certified', 'why-5d': 'Fully certified for EU, Middle East and Australia markets. Test reports provided with every order.',

      'why-6h': '50+ Countries Served', 'why-6d': 'Active distribution in Saudi Arabia, UAE, Iraq, UK, France, Germany, Australia, and more.',

      'oem-tag': 'OEM / ODM PARTNER', 'oem-title': 'Your Brand,<br>Our Manufacturing',

      'oem-desc': 'We manufacture and brand fans under your label. From concept to carton, BAER handles tooling, production, testing and packaging.',

      'oem-moq': 'Minimum Order Qty', 'oem-sample': 'Sample Turnaround', 'oem-lead': 'Mass Production Lead', 'oem-qc': 'Pre-Ship QC Inspection',

      'oem-cta': 'Start OEM Discussion',

      'review-tag': 'CLIENT FEEDBACK', 'review-title': 'What Our Partners Say',

      'faq-tag': 'BUYER FAQ', 'faq-title': 'Frequently Asked Questions',

      'faq-q1': 'What is the minimum order quantity (MOQ)?', 'faq-a1': 'Standard stock models: MOQ 100 pcs. OEM/custom models: MOQ 500 pcs. Flexible for first orders.',

      'faq-q2': 'Do you provide CE and RoHS certificates?', 'faq-a2': 'Yes. All standard models carry CE and RoHS certification. Test reports provided with every shipment.',

      'faq-q3': 'What is the lead time for mass production?', 'faq-a3': 'Standard production: 25–35 days. OEM/custom mold orders: 45–60 days. In-stock models: 3–7 days.',

      'faq-q4': 'Can you customize voltage for different countries?', 'faq-a4': 'Yes. We support 110V/60Hz, 220–240V/50Hz, and custom voltage requirements.',

      'faq-q5': 'What warranty do you offer?', 'faq-a5': '2-year warranty on all products. Defective units replaced or refunded after confirmation.'

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

      'inq-type': 'نوع المنتج', 'inq-req': 'المتطلبات التفصيلية', 'inq-submit': 'إرسال الاستفسار',

      'cert-tag': 'معتمد ومتوافق', 'cert-title': 'شهادات الجودة الدولية',

      'cert-desc': 'كل منتج BAER يخضع للاختبار والاعتماد وفق أعلى معايير السلامة العالمية.',

      'cert-ce': 'دخول السوق الأوروبي', 'cert-3c': 'شهادة إلزامية صينية', 'cert-iso': 'إدارة الجودة',

      'cert-cb': 'سلامة IEC العالمية', 'cert-saa': 'معتمد في أستراليا', 'cert-etl': 'مدرج في أمريكا الشمالية',

      'cert-note': '* الشهادات متاحة عند الطلب مع كل طلبية',

      'app-tag': 'مجالات الاستخدام', 'app-title': 'سيناريوهات التطبيق',

      'app-desc': 'تُستخدم مراوح BAER في البيئات السكنية والتجارية والصناعية عبر أكثر من 50 دولة.',

      'app-1': 'سكني', 'app-1d': 'غرفة النوم · المطبخ · الحمام',

      'app-2': 'صناعي', 'app-2d': 'مصنع · ورشة · مستودع',

      'app-3': 'تجاري', 'app-3d': 'مكتب · مول · فندق · مطعم',

      'app-4': 'رعاية صحية', 'app-4d': 'مستشفى · عيادة · صيدلية',

      'app-5': 'مشاريع HVAC', 'app-5d': 'هواء نقي · استعادة الحرارة · جودة الهواء الداخلي',

      'why-tag': 'لماذا BAER', 'why-title': 'لماذا يختارنا المشترون العالميون',

      'why-1h': 'مباشر من المصنع', 'why-1d': 'مصنع خاص 50,000م² في زيجيانغ. بدون وسطاء — أسعار أقل بنسبة 15–30% مقارنة بشركات التجارة.',

      'why-2h': 'قدرة OEM / ODM', 'why-2d': 'شعار مخصص، ألوان، جهد، تصميم شفرة، وتغليف. الحد الأدنى للطلب 500 قطعة.',

      'why-3h': 'وقت تسليم سريع', 'why-3d': 'عينة في 7 أيام. إنتاج ضخم في 25–35 يوماً. النماذج الجاهزة ترسل خلال 3 أيام.',

      'why-4h': 'ضمان سنتين', 'why-4d': 'ضمان سنتين على جميع المنتجات. الوحدات المعيبة تُستبدل أو تُرد خلال 30 يوماً.',

      'why-5h': 'معتمد CE / RoHS', 'why-5d': 'معتمد بالكامل للأسواق الأوروبية والشرق أوسطية والأسترالية. تقارير الاختبار مرفقة مع كل طلب.',

      'why-6h': '+50 دولة تخدمها', 'why-6d': 'توزيع نشط في المملكة العربية السعودية والإمارات والعراق والمملكة المتحدة وفرنسا وألمانيا وأستراليا.',

      'oem-tag': 'شريك OEM / ODM', 'oem-title': 'علامتك التجارية،<br>تصنيعنا',

      'oem-desc': 'نصنع المراوح تحت علامتك التجارية. من الفكرة إلى الكرتون، BAER تتولى القوالب والإنتاج والاختبار والتغليف.',

      'oem-moq': 'الحد الأدنى للطلب', 'oem-sample': 'وقت تسليم العينة', 'oem-lead': 'مدة الإنتاج الضخم', 'oem-qc': 'فحص الجودة قبل الشحن',

      'oem-cta': 'ابدأ مناقشة OEM',

      'review-tag': 'آراء العملاء', 'review-title': 'ماذا يقول شركاؤنا',

      'faq-tag': 'أسئلة المشترين', 'faq-title': 'الأسئلة الشائعة',

      'faq-q1': 'ما هو الحد الأدنى لكمية الطلب؟', 'faq-a1': 'النماذج القياسية المتوفرة: 100 قطعة. نماذج OEM المخصصة: 500 قطعة. مرونة في الطلبات الأولى.',

      'faq-q2': 'هل تقدمون شهادات CE و RoHS؟', 'faq-a2': 'نعم. جميع النماذج القياسية معتمدة CE و RoHS. تقارير الاختبار مرفقة مع كل شحنة.',

      'faq-q3': 'ما هو وقت التسليم للإنتاج الضخم؟', 'faq-a3': 'الإنتاج القياسي: 25–35 يوماً. طلبات OEM المخصصة: 45–60 يوماً. النماذج الجاهزة: 3–7 أيام.',

      'faq-q4': 'هل يمكنكم تخصيص الجهد الكهربائي لدول مختلفة؟', 'faq-a4': 'نعم. ندعم 110V/60Hz و220-240V/50Hz ومتطلبات جهد مخصصة.',

      'faq-q5': 'ما هو الضمان المقدم؟', 'faq-a5': 'ضمان سنتين على جميع المنتجات. الوحدات المعيبة تُستبدل أو تُرد بعد التأكيد.'

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

      'inq-type': '产品类型', 'inq-req': '详细需求', 'inq-submit': '提交询盘',

      'cert-tag': '认证与合规', 'cert-title': '国际质量认证',

      'cert-desc': '每款 BAER 产品均经过测试和认证，符合全球安全与性能标准。',

      'cert-ce': 'EU市场准入', 'cert-3c': '中国强制性认证', 'cert-iso': '质量管理体系',

      'cert-cb': 'IEC国际安全认证', 'cert-saa': '澳大利亚认证', 'cert-etl': '北美市场认证',

      'cert-note': '* 每批订单均可提供认证报告',

      'app-tag': '应用领域', 'app-title': '应用场景',

      'app-desc': 'BAER 换气扇广泛应用于全球50+国家的住宅、商业及工业场所。',

      'app-1': '住宅', 'app-1d': '卧室 · 厨房 · 卫浴',

      'app-2': '工业', 'app-2d': '工厂 · 车间 · 仓库',

      'app-3': '商业', 'app-3d': '办公室 · 商场 · 酒店 · 餐厅',

      'app-4': '医疗', 'app-4d': '医院 · 诊所 · 药房',

      'app-5': '暖通项目', 'app-5d': '新风系统 · 全热交换 · 室内空气质量',

      'why-tag': '为什么选择 BAER', 'why-title': '全球买家为何选择我们',

      'why-1h': '工厂直供', 'why-1d': '浙江自有工厂50,000m²，无中间商，比贸易公司价格低15–30%。',

      'why-2h': 'OEM / ODM 能力', 'why-2d': '定制Logo、颜色、电压、叶轮设计和包装，起订量500件，支持全套贴牌服务。',

      'why-3h': '交期保障', 'why-3d': '样品7天，批量生产25–35天，现货3天内发货，灵活应对季节性需求。',

      'why-4h': '2年质保', 'why-4d': '所有产品2年质保，30天内确认缺陷即换货或退款，终身技术支持。',

      'why-5h': 'CE / RoHS 认证', 'why-5d': '全面认证，满足欧盟、中东、澳大利亚市场要求，每笔订单随附检测报告。',

      'why-6h': '服务50+国家', 'why-6d': '活跃于沙特、UAE、伊拉克、英国、法国、德国、澳大利亚等市场。',

      'oem-tag': 'OEM / ODM 合作伙伴', 'oem-title': '您的品牌，<br>我们的制造',

      'oem-desc': '我们在您的品牌下生产风机。从方案到包装，BAER全程负责开模、生产、测试和包装。',

      'oem-moq': '最小起订量', 'oem-sample': '样品交期', 'oem-lead': '量产交期', 'oem-qc': '出货前100%质检',

      'oem-cta': '开始OEM合作咨询',

      'review-tag': '客户反馈', 'review-title': '合作伙伴怎么说',

      'faq-tag': '买家常见问题', 'faq-title': '常见问题解答',

      'faq-q1': '最小起订量（MOQ）是多少？', 'faq-a1': '标准现货型号：100件起。OEM定制型号：500件起。首次合作和样品订单可灵活协商。',

      'faq-q2': '提供CE和RoHS认证吗？', 'faq-a2': '是的。所有标准型号均持有CE和RoHS认证，每批货随附检测报告和符合性声明。',

      'faq-q3': '量产交期是多久？', 'faq-a3': '标准批量：25–35天；OEM开模定制：45–60天；现货型号：3–7天。',

      'faq-q4': '可以定制适配不同国家的电压吗？', 'faq-a4': '可以。支持110V/60Hz、220–240V/50Hz及定制电压，在询盘中注明即可。',

      'faq-q5': '提供什么质保？', 'faq-a5': '所有产品2年质保，经确认的缺陷单位30天内换货或退款，同时提供终身技术支持和备件供应。'

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

