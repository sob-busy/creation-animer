/* ==========================================================================
   Création d'Animer — interactions
   ========================================================================== */
(function () {
  'use strict';

  var WHATSAPP_NUMBER = '22892355735';
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* Logo : on utilise assets/img/logo.png s'il existe, sinon le SVG provisoire */
  $$('.logo-img').forEach(function (img) {
    var fallback = function () {
      if (img.dataset.fallback) return;
      img.dataset.fallback = '1';
      img.src = 'assets/img/logo.svg';
    };
    img.addEventListener('error', fallback);
    if (img.complete && img.naturalWidth === 0) fallback();
  });

  /* Année du pied de page */
  var year = $('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  /* ------------------------------------------------------------------------
     Titre découpé en mots
     ------------------------------------------------------------------------ */
  $$('[data-split]').forEach(function (el) {
    var i = 0;
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var outer = document.createElement('span');
            var inner = document.createElement('span');
            outer.className = 'split-word';
            inner.textContent = part;
            inner.style.transitionDelay = (0.25 + i++ * 0.07) + 's';
            outer.appendChild(inner);
            frag.appendChild(outer);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1 && child.tagName !== 'BR') {
          walk(child);
        }
      });
    };
    walk(el);
  });

  /* ------------------------------------------------------------------------
     Écran d'intro
     ------------------------------------------------------------------------ */
  var counter = $('[data-loader-count]');
  var finishLoading = function () {
    document.body.classList.remove('is-loading');
    document.body.classList.add('is-loaded');
  };

  if (reduceMotion || !counter) {
    finishLoading();
  } else {
    var start = null;
    var duration = 1100;
    var tick = function (t) {
      if (!start) start = t;
      var p = Math.min((t - start) / duration, 1);
      counter.textContent = Math.round((1 - Math.pow(1 - p, 3)) * 100);
      if (p < 1) requestAnimationFrame(tick);
      else setTimeout(finishLoading, 180);
    };
    requestAnimationFrame(tick);
  }

  /* ------------------------------------------------------------------------
     En-tête : fond au défilement, masqué en descendant
     ------------------------------------------------------------------------ */
  var header = $('[data-header]');
  var progress = $('.progress span');
  var waFloat = $('.wa-float');
  var lastY = window.scrollY;
  var ticking = false;
  var parallaxEls = $$('[data-parallax]');
  var stepsLine = $('[data-steps-line]');
  var stepsWrap = $('.steps');

  var onScroll = function () {
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var menuOpen = document.body.classList.contains('menu-open');

    header.classList.toggle('is-scrolled', y > 30);
    if (!menuOpen) header.classList.toggle('is-hidden', y > lastY && y > 400);
    if (progress) progress.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (waFloat) waFloat.classList.toggle('is-visible', y > window.innerHeight * 0.6);

    if (!reduceMotion) {
      parallaxEls.forEach(function (el) {
        el.style.transform = 'translate3d(0,' + (y * parseFloat(el.dataset.parallax)) + 'px,0)';
      });
    }

    if (stepsLine && stepsWrap) {
      var r = stepsWrap.getBoundingClientRect();
      var p = (window.innerHeight * 0.8 - r.top) / (r.height + window.innerHeight * 0.3);
      stepsLine.style.transform = 'scaleX(' + Math.max(0, Math.min(1, p)) + ')';
    }

    lastY = y;
    ticking = false;
  };
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ------------------------------------------------------------------------
     Menu mobile
     ------------------------------------------------------------------------ */
  var burger = $('[data-burger]');
  var nav = $('[data-nav]');
  var setMenu = function (open) {
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) header.classList.remove('is-hidden');
  };
  burger.addEventListener('click', function () {
    setMenu(burger.getAttribute('aria-expanded') !== 'true');
  });
  $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); burger.focus(); }
  });

  /* Lien actif selon la section visible */
  var navLinks = $$('.nav ul a');
  if ('IntersectionObserver' in window) {
    var sectionObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle('is-current', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    navLinks.forEach(function (a) {
      var s = $(a.getAttribute('href'));
      if (s) sectionObs.observe(s);
    });
  }

  /* ------------------------------------------------------------------------
     Apparitions au défilement + compteurs
     ------------------------------------------------------------------------ */
  var animateCount = function (el) {
    var target = parseInt(el.dataset.count, 10);
    if (reduceMotion) { el.textContent = target; return; }
    var t0 = null;
    var step = function (t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1600, 1);
      el.textContent = Math.round((1 - Math.pow(1 - p, 4)) * target);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // Décalage en cascade des éléments frères
  $$('.reveal').forEach(function (el) {
    var siblings = $$(':scope > .reveal', el.parentElement);
    var idx = siblings.indexOf(el);
    if (idx > 0) el.style.setProperty('--d', Math.min(idx * 0.08, 0.4) + 's');
  });

  if ('IntersectionObserver' in window) {
    var revealObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        $$('[data-count]', entry.target).forEach(animateCount);
        revealObs.unobserve(entry.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal').forEach(function (el) { revealObs.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
    $$('[data-count]').forEach(function (el) { el.textContent = el.dataset.count; });
  }

  /* ------------------------------------------------------------------------
     Filtres des réalisations
     ------------------------------------------------------------------------ */
  var filters = $$('[data-filter]');
  var cards = $$('.card[data-cat]');
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var cat = btn.dataset.filter;
      filters.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-pressed', String(on));
      });
      cards.forEach(function (c) { c.classList.add('is-filtering'); });
      setTimeout(function () {
        cards.forEach(function (c) {
          var show = cat === 'all' || c.dataset.cat === cat;
          c.classList.toggle('is-hidden', !show);
          c.classList.add('is-visible');
        });
        requestAnimationFrame(function () {
          cards.forEach(function (c) { c.classList.remove('is-filtering'); });
        });
      }, reduceMotion ? 0 : 280);
    });
  });

  /* ------------------------------------------------------------------------
     Avis clients
     ------------------------------------------------------------------------ */
  var slider = $('[data-slider]');
  if (slider) {
    var quotes = $$('.quote', slider);
    var current = 0;
    var timer;
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    $('[data-total]', slider).textContent = pad(quotes.length);
    var go = function (i) {
      quotes[current].classList.remove('is-active');
      current = (i + quotes.length) % quotes.length;
      quotes[current].classList.add('is-active');
      $('[data-current]', slider).textContent = pad(current + 1);
    };
    var auto = function () {
      clearInterval(timer);
      if (!reduceMotion) timer = setInterval(function () { go(current + 1); }, 7000);
    };
    $('[data-next]', slider).addEventListener('click', function () { go(current + 1); auto(); });
    $('[data-prev]', slider).addEventListener('click', function () { go(current - 1); auto(); });
    slider.addEventListener('mouseenter', function () { clearInterval(timer); });
    slider.addEventListener('mouseleave', auto);
    auto();
  }

  /* ------------------------------------------------------------------------
     FAQ : une seule question ouverte à la fois
     ------------------------------------------------------------------------ */
  var faqItems = $$('.faq__item');
  faqItems.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (d.open) faqItems.forEach(function (o) { if (o !== d) o.open = false; });
    });
  });

  /* ------------------------------------------------------------------------
     Formulaire → WhatsApp
     ------------------------------------------------------------------------ */
  var form = $('[data-contact-form]');
  if (form) {
    var status = $('[data-form-status]', form);
    var validate = function (field) {
      var input = $('input, textarea', field);
      var ok = input.checkValidity() && (!input.required || input.value.trim() !== '');
      field.classList.toggle('has-error', !ok);
      return ok;
    };
    $$('.field', form).forEach(function (f) {
      $('input, textarea', f).addEventListener('blur', function () { validate(f); });
      $('input, textarea', f).addEventListener('input', function () {
        if (f.classList.contains('has-error')) validate(f);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fields = $$('.field', form);
      var valid = fields.map(validate).every(Boolean);
      if (!valid) {
        status.textContent = 'Merci de compléter les champs indiqués.';
        var firstErr = $('.has-error input, .has-error textarea', form);
        if (firstErr) firstErr.focus();
        return;
      }
      var data = new FormData(form);
      var needs = data.getAll('need');
      var lines = [
        'Bonjour Création d\'Animer,',
        '',
        'Je m\'appelle ' + data.get('name').trim() + '.'
      ];
      if (needs.length) lines.push('Besoin : ' + needs.join(', '));
      lines.push('', data.get('message').trim());
      if (data.get('phone')) lines.push('', 'Mon numéro : ' + data.get('phone').trim());

      var url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
      window.open(url, '_blank', 'noopener');
      status.textContent = 'WhatsApp s\'ouvre avec votre message. Il ne reste qu\'à appuyer sur « Envoyer ».';
      form.reset();
    });
  }

  /* ------------------------------------------------------------------------
     Curseur personnalisé + boutons magnétiques (souris uniquement)
     ------------------------------------------------------------------------ */
  if (finePointer && !reduceMotion) {
    var cursor = $('.cursor');
    var label = $('.cursor__label');
    var mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      cursor.classList.add('is-visible');
    }, { passive: true });
    document.addEventListener('mouseleave', function () { cursor.classList.remove('is-visible'); });
    (function loop() {
      cx += (mx - cx) * 0.18;
      cy += (my - cy) * 0.18;
      cursor.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)';
      requestAnimationFrame(loop);
    })();
    $$('[data-cursor]').forEach(function (el) {
      el.addEventListener('mouseenter', function () { label.textContent = el.dataset.cursor; cursor.classList.add('is-big'); });
      el.addEventListener('mouseleave', function () { cursor.classList.remove('is-big'); });
    });

    $$('.magnetic').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.25;
        var y = (e.clientY - r.top - r.height / 2) * 0.35;
        el.style.transform = 'translate(' + x + 'px,' + y + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }
})();
