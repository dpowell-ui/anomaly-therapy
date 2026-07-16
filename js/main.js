/* ============================================================
   ANOMALY THERAPY — INTERACTIONS
   ============================================================ */

(() => {
  /* ---------- Mobile menu ---------- */
  const toggle = document.querySelector('.menu-toggle');
  const menu   = document.querySelector('.mobile-menu');

  if (toggle && menu) {
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      menu.dataset.open = String(open);
      document.body.style.overflow = open ? 'hidden' : '';
    };

    toggle.addEventListener('click', () => {
      const isOpen = toggle.getAttribute('aria-expanded') === 'true';
      setOpen(!isOpen);
    });

    menu.querySelectorAll('a').forEach((a) => {
      a.addEventListener('click', () => setOpen(false));
    });
  }

  /* ---------- Floating "Book a Consult" CTA ----------
     Appears after the user has scrolled past the hero, hides at very top */
  const floatCta = document.querySelector('.float-cta');

  if (floatCta) {
    const onScroll = () => {
      const shouldShow = window.scrollY > 480;
      floatCta.dataset.visible = String(shouldShow);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Accessible care popup ----------
     - Appears 3s after page load OR when user scrolls 40% down (whichever first)
     - Dismissible; remembers dismissal for 7 days via localStorage
     - Hidden on Contact page so it doesn't compete with the main CTAs */
  const popup = document.querySelector('.popup');

  if (popup) {
    const KEY = 'anomaly_popup_dismissed_at';
    const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;

    let dismissed = false;
    try {
      const ts = parseInt(localStorage.getItem(KEY) || '0', 10);
      dismissed = ts && (Date.now() - ts) < SEVEN_DAYS;
    } catch (e) { /* localStorage unavailable */ }

    if (!dismissed) {
      let opened = false;
      const open = () => {
        if (opened) return;
        opened = true;
        popup.dataset.open = 'true';
      };

      const close = () => {
        popup.dataset.open = 'false';
        try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
      };

      // Time-based trigger
      setTimeout(open, 3000);

      // Scroll-based trigger
      const onScroll = () => {
        const scrolled = window.scrollY + window.innerHeight;
        const total = document.documentElement.scrollHeight;
        if (scrolled / total > 0.4) {
          open();
          window.removeEventListener('scroll', onScroll);
        }
      };
      window.addEventListener('scroll', onScroll, { passive: true });

      const closeBtn = popup.querySelector('.popup__close');
      if (closeBtn) closeBtn.addEventListener('click', close);
    }
  }

  /* ---------- Reveal on scroll ---------- */
  const revealEls = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.dataset.visible = 'true';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => { el.dataset.visible = 'true'; });
  }

  /* ---------- Team card hover-cycle ----------
     Cards with multiple stacked photos cycle through them on hover */
  document.querySelectorAll('.member[data-photos]').forEach((card) => {
    const imgs = card.querySelectorAll('.member__photo img');
    if (imgs.length < 2) return;

    imgs[0].classList.add('is-current');
    let idx = 0;
    let timer = null;

    const advance = () => {
      imgs[idx].classList.remove('is-current');
      idx = (idx + 1) % imgs.length;
      imgs[idx].classList.add('is-current');
    };

    const reset = () => {
      if (timer) { clearInterval(timer); timer = null; }
      imgs[idx].classList.remove('is-current');
      idx = 0;
      imgs[idx].classList.add('is-current');
    };

    card.addEventListener('mouseenter', () => {
      if (timer) return;
      advance();
      timer = setInterval(advance, 1400);
    });

    card.addEventListener('mouseleave', reset);
    card.addEventListener('focusout', reset);
  });

  /* ---------- Mark current nav ---------- */
  const path = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('[data-nav-path]').forEach((a) => {
    const target = a.dataset.navPath.replace(/\/$/, '') || '/';
    if (path === target || (target !== '/' && path.startsWith(target))) {
      a.setAttribute('aria-current', 'page');
    }
  });
})();
