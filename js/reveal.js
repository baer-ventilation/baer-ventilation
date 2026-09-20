/* BAER scroll-reveal (v1) - progressive enhancement, no-JS users & crawlers see full content */
(function () {
  try {
    if (!('IntersectionObserver' in window)) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!Element.prototype.closest) return;

    var style = document.createElement('style');
    style.textContent = '.rv{opacity:0;transform:translateY(26px);transition:opacity .6s ease,transform .6s ease}.rv.rv-in{opacity:1;transform:none}';
    document.head.appendChild(style);

    var units = [];
    var seen = [];
    function add(el) {
      if (!el || el.classList.contains('rv')) return;
      for (var i = 0; i < seen.length; i++) {
        if (el === seen[i] || el.contains(seen[i]) || seen[i].contains(el)) return;
      }
      seen.push(el);
      units.push(el);
    }
    document.querySelectorAll('section, article').forEach(add);
    document.querySelectorAll('h1, h2, table, details, form, footer').forEach(function (e) {
      if (!e.closest('section, article')) add(e);
    });
    if (!units.length) return;

    var vh = window.innerHeight || 800;
    var batch = 0;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        io.unobserve(el);
        el.style.transitionDelay = Math.min(batch * 80, 240) + 'ms';
        batch++;
        el.classList.add('rv-in');
        el.addEventListener('transitionend', function h() {
          el.style.transitionDelay = '';
          el.removeEventListener('transitionend', h);
        });
      });
      if (batch > 6) batch = 0;
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    units.forEach(function (el) {
      if (el.getBoundingClientRect().height > vh * 2) return;
      el.classList.add('rv');
      io.observe(el);
    });
  } catch (e) { /* never break the page */ }
})();
