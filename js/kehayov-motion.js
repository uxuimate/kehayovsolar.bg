(function () {
  'use strict';
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.kehayov-enter-group').forEach(function (group) {
    group.querySelectorAll('.kehayov-enter').forEach(function (el, i) {
      el.style.setProperty('--nt-enter-delay', (i * 68) + 'ms');
    });
  });

  var motionEls = [];
  var seen = new Set();
  function addMotionEl(el) {
    if (seen.has(el)) return;
    seen.add(el);
    motionEls.push(el);
  }
  document.querySelectorAll('.kehayov-reveal').forEach(addMotionEl);
  document.querySelectorAll('.kehayov-enter').forEach(addMotionEl);
  if (!motionEls.length) return;

  if (reduceMotion || !('IntersectionObserver' in window)) {
    motionEls.forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('is-visible');
        io.unobserve(en.target);
      }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

  motionEls.forEach(function (el) {
    io.observe(el);
  });
})();

(function ($) {
  if (!$ || !$.fn.owlCarousel) return;
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isBg = (document.documentElement.lang || '').toLowerCase().indexOf('bg') === 0;

  var $brands = $('.ks-brands-slider');
  if ($brands.length) {
    $brands.owlCarousel({
      items: 1,
      loop: true,
      margin: 0,
      dots: true,
      nav: true,
      navText: ['', ''],
      smartSpeed: 650,
      autoplay: !reduceMotion,
      autoplayTimeout: 5600,
      autoplayHoverPause: true
    });
  }

  var $proof = $('.ks-proof-slider');
  if ($proof.length) {
    $proof.owlCarousel({
      loop: true,
      margin: 16,
      dots: true,
      nav: true,
      navText: [
        '<span aria-hidden="true">‹</span><span class="sr-only">' + (isBg ? 'Предишни снимки' : 'Previous photos') + '</span>',
        '<span aria-hidden="true">›</span><span class="sr-only">' + (isBg ? 'Следващи снимки' : 'Next photos') + '</span>'
      ],
      smartSpeed: 500,
      autoplay: !reduceMotion,
      autoplayTimeout: 6200,
      autoplayHoverPause: true,
      responsive: {
        0: { items: 1 },
        640: { items: 2 },
        992: { items: 3 }
      }
    });
  }

  var $packages = $('.ks-packages-slider');
  if ($packages.length) {
    var pkgPrev = isBg ? 'Предишен пакет' : 'Previous package';
    var pkgNext = isBg ? 'Следващ пакет' : 'Next package';

    function syncPackageNav(event) {
      var owl = event.relatedTarget;
      var visible = owl.settings.items;
      var total = owl.items().length;
      var $nav = $(event.target).find('.owl-nav');
      var $dots = $(event.target).find('.owl-dots');
      if (total <= visible) {
        $nav.addClass('disabled').attr('aria-hidden', 'true');
        $dots.addClass('disabled').attr('aria-hidden', 'true');
      } else {
        $nav.removeClass('disabled').removeAttr('aria-hidden');
        $dots.removeClass('disabled').removeAttr('aria-hidden');
      }
    }

    $packages.owlCarousel({
      loop: false,
      rewind: false,
      margin: 20,
      dots: true,
      nav: true,
      autoHeight: false,
      navText: [
        '<span aria-hidden="true">‹</span><span class="sr-only">' + pkgPrev + '</span>',
        '<span aria-hidden="true">›</span><span class="sr-only">' + pkgNext + '</span>'
      ],
      smartSpeed: 450,
      autoplay: false,
      mouseDrag: true,
      touchDrag: true,
      responsive: {
        0: { items: 1 },
        640: { items: 2 },
        992: { items: 3 },
        1200: { items: 4 }
      },
      onInitialized: syncPackageNav,
      onResized: syncPackageNav
    });
  }
})(window.jQuery);

(function () {
  var slider = document.getElementById('rev_slider');
  if (!slider || !('IntersectionObserver' in window)) return;

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      slider.querySelectorAll('video').forEach(function (video) {
        if (en.isIntersecting) {
          var play = video.play();
          if (play && play.catch) play.catch(function () {});
        } else {
          video.pause();
        }
      });
    });
  }, { threshold: 0.12 });

  io.observe(slider);
})();

(function () {
  var gallery = document.getElementById('ks-gallery');
  if (!gallery) return;
  var buttons = document.querySelectorAll('.ks-gallery-filters__btn');
  var items = gallery.querySelectorAll('.ks-gallery-item');
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var filter = btn.getAttribute('data-filter') || 'all';
      buttons.forEach(function (b) { b.classList.toggle('is-active', b === btn); });
      items.forEach(function (item) {
        var cat = item.getAttribute('data-cat');
        var show = filter === 'all' || cat === filter;
        item.classList.toggle('is-hidden', !show);
      });
    });
  });
})();

(function () {
  var rings = document.querySelectorAll('.ks-about-company__orbit');
  if (!rings.length) return;
  rings.forEach(function (text) {
    var chars = (text.textContent || '').trim().split('');
    if (!chars.length) return;
    var step = 360 / chars.length;
    text.innerHTML = chars.map(function (char, i) {
      var safe = char === ' ' ? '&nbsp;' : char.replace(/</g, '&lt;');
      return '<span style="transform:rotate(' + (i * step) + 'deg)">' + safe + '</span>';
    }).join('');
  });
})();

(function () {
  function showHint(el) {
    if (!el) return;
    el.hidden = false;
    el.removeAttribute('hidden');
  }

  function hideHint(el) {
    if (!el) return;
    el.hidden = true;
    el.setAttribute('hidden', '');
  }

  function syncPackageHint() {
    var hint = document.querySelector('[data-ks-hint="packages"]');
    var slider = document.querySelector('.ks-packages-slider');
    if (!hint || !slider || !window.jQuery) return;
    var $s = window.jQuery(slider);
    if (!$s.data('owl.carousel')) {
      hideHint(hint);
      return;
    }
    var owl = $s.data('owl.carousel');
    var visible = owl.settings.items;
    var total = owl.items().length;
    if (window.matchMedia('(max-width: 1199px)').matches && total > visible) {
      showHint(hint);
    } else {
      hideHint(hint);
    }
  }

  function syncSystemHint() {
    var hint = document.querySelector('[data-ks-hint="systems"]');
    var stage = document.querySelector('.ks-system-stage');
    if (!hint || !stage) return;
    var needsScroll =
      window.matchMedia('(max-width: 991px)').matches &&
      stage.scrollWidth > stage.clientWidth + 8;
    if (needsScroll) showHint(hint);
    else hideHint(hint);
  }

  function syncAll() {
    syncPackageHint();
    syncSystemHint();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(syncAll, 400);
    });
  } else {
    setTimeout(syncAll, 400);
  }
  window.addEventListener('resize', syncAll);
  if (window.jQuery) {
    window.jQuery(document).on(
      'initialized.owl.carousel resized.owl.carousel',
      '.ks-packages-slider',
      syncPackageHint
    );
  }
})();
