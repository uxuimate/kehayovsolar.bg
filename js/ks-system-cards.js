(function () {
  'use strict';

  var cards = document.querySelectorAll('[data-ks-scene]');
  if (!cards.length) return;

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var THREE = window.THREE;

  cards.forEach(function (card) {
    var media = card.querySelector('.ks-sys-card__media');
    if (!media) return;

    var rx = 0;
    var ry = 0;
    var tx = 0;
    var ty = 0;

    function onMove(e) {
      var rect = media.getBoundingClientRect();
      tx = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      ty = ((e.clientY - rect.top) / rect.height - 0.5) * 2;
    }

    function onLeave() {
      tx = 0;
      ty = 0;
    }

    media.addEventListener('mousemove', onMove);
    media.addEventListener('mouseleave', onLeave);

    function tiltTick() {
      rx += (ty * -6 - rx) * 0.08;
      ry += (tx * 8 - ry) * 0.08;
      media.style.setProperty('--ks-rx', rx.toFixed(3) + 'deg');
      media.style.setProperty('--ks-ry', ry.toFixed(3) + 'deg');
      if (!reduceMotion) requestAnimationFrame(tiltTick);
    }
    if (!reduceMotion) requestAnimationFrame(tiltTick);
  });

  if (!THREE) return;

  var LIME = new THREE.Color(0xcee002);
  var runtimes = [];
  var byCard = typeof WeakMap === 'function' ? new WeakMap() : null;

  function makeField(kind) {
    var n = kind === 'storage' ? 56 : 48;
    var positions = new Float32Array(n * 3);
    var speeds = new Float32Array(n);
    var i;
    for (i = 0; i < n; i++) {
      positions[i * 3] = Math.random() * 2 - 1;
      positions[i * 3 + 1] = Math.random() * 2 - 1;
      positions[i * 3 + 2] = Math.random() * 0.4 - 0.15;
      speeds[i] = 0.12 + Math.random() * 0.22;
    }
    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    var mat = new THREE.PointsMaterial({
      color: LIME,
      size: 0.028,
      transparent: true,
      opacity: 0.72,
      depthWrite: false,
      blending: THREE.AdditiveBlending
    });
    var points = new THREE.Points(geo, mat);

    return {
      points: points,
      n: n,
      speeds: speeds,
      update: function (t, pointer) {
        var arr = geo.attributes.position.array;
        var j;
        for (j = 0; j < n; j++) {
          if (kind === 'grid') {
            arr[j * 3] += speeds[j] * 0.008;
            if (arr[j * 3] > 1.15) arr[j * 3] = -1.15;
            arr[j * 3 + 1] += Math.sin(t * 0.7 + j) * 0.0008;
          } else if (kind === 'hybrid') {
            arr[j * 3] += (j % 2 ? 1 : -1) * speeds[j] * 0.006;
            arr[j * 3 + 1] += speeds[j] * 0.003;
            if (arr[j * 3] > 1.2) arr[j * 3] = -1.2;
            if (arr[j * 3] < -1.2) arr[j * 3] = 1.2;
            if (arr[j * 3 + 1] > 1.2) arr[j * 3 + 1] = -1.2;
          } else if (kind === 'offgrid') {
            arr[j * 3] += Math.sin(t * 0.4 + j) * 0.0012;
            arr[j * 3 + 1] += Math.cos(t * 0.35 + j) * 0.001;
          } else {
            arr[j * 3 + 1] += speeds[j] * 0.007;
            if (arr[j * 3 + 1] > 1.2) arr[j * 3 + 1] = -1.2;
          }
          arr[j * 3] += pointer.x * 0.0015;
          arr[j * 3 + 1] += pointer.y * 0.0015;
        }
        geo.attributes.position.needsUpdate = true;
        points.rotation.y = pointer.x * 0.08;
        points.rotation.x = pointer.y * -0.06;
      }
    };
  }

  cards.forEach(function (card) {
    var canvas = card.querySelector('canvas');
    var kind = card.getAttribute('data-ks-scene') || 'grid';
    if (!canvas) return;

    var scene = new THREE.Scene();
    var camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 10);
    camera.position.z = 2;
    var field = makeField(kind);
    scene.add(field.points);

    var renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.setClearColor(0x000000, 0);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));

    var pointer = { x: 0, y: 0 };
    var target = { x: 0, y: 0 };
    var visible = true;

    function size() {
      var w = canvas.clientWidth;
      var h = canvas.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
    }

    card.addEventListener('mousemove', function (e) {
      var rect = card.getBoundingClientRect();
      target.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      target.y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
    });
    card.addEventListener('mouseleave', function () {
      target.x = 0;
      target.y = 0;
    });

    var runtime = {
      renderer: renderer,
      scene: scene,
      camera: camera,
      field: field,
      pointer: pointer,
      target: target,
      size: size,
      visible: function () { return visible; },
      setVisible: function (v) { visible = v; }
    };
    runtimes.push(runtime);
    if (byCard) byCard.set(card, runtime);

    if ('ResizeObserver' in window) new ResizeObserver(size).observe(card);
    size();
  });

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var rt = byCard ? byCard.get(en.target) : null;
        if (rt) rt.setVisible(en.isIntersecting);
      });
    }, { threshold: 0.08 });
    cards.forEach(function (card) { io.observe(card); });
  }

  var t0 = performance.now();
  function tick(now) {
    var t = (now - t0) / 1000;
    runtimes.forEach(function (rt) {
      if (!rt.visible()) return;
      rt.size();
      rt.pointer.x += (rt.target.x - rt.pointer.x) * 0.08;
      rt.pointer.y += (rt.target.y - rt.pointer.y) * 0.08;
      rt.field.update(reduceMotion ? 0 : t, rt.pointer);
      rt.renderer.render(rt.scene, rt.camera);
    });
    if (!reduceMotion) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
