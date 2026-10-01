/**
 * TRAVELISTIC - JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  /* --------------------------------------------------------------------------
     1. STICKY HEADER & SCROLL BEHAVIORS
     -------------------------------------------------------------------------- */
  const header = document.querySelector('.header');
  const backToTopBtn = document.querySelector('.back-to-top');
  const readingProgressBar = document.querySelector('.reading-progress-bar');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    // Sticky header background
    if (header) {
      if (scrollY > 60) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }

    // Back to top button visibility
    if (backToTopBtn) {
      if (scrollY > 400) {
        backToTopBtn.classList.add('active');
      } else {
        backToTopBtn.classList.remove('active');
      }
    }

    // Reading progress bar for single blog post
    if (readingProgressBar) {
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = (scrollY / docHeight) * 100;
      readingProgressBar.style.width = `${progress}%`;
    }
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  /* --------------------------------------------------------------------------
     2. MOBILE NAVIGATION DRAWER
     -------------------------------------------------------------------------- */
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');
  const dropdownParents = document.querySelectorAll('.has-dropdown');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      const icon = hamburger.querySelector('i');
      if (icon) {
        if (navMenu.classList.contains('active')) {
          icon.classList.remove('fa-bars');
          icon.classList.add('fa-times');
        } else {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!header.contains(e.target) && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        const icon = hamburger.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-times');
          icon.classList.add('fa-bars');
        }
      }
    });

    // Mobile dropdown toggle
    dropdownParents.forEach(item => {
      const link = item.querySelector('.nav-link');
      if (link) {
        link.addEventListener('click', (e) => {
          if (window.innerWidth <= 768) {
            e.preventDefault();
            item.classList.toggle('open');
          }
        });
      }
    });
  }

  /* --------------------------------------------------------------------------
     2.1. LANGUAGE SWITCHER DROPDOWNS
     -------------------------------------------------------------------------- */
  const langSwitchers = document.querySelectorAll('.lang-switcher');
  langSwitchers.forEach(switcher => {
    const btn = switcher.querySelector('.lang-btn');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        langSwitchers.forEach(s => {
          if (s !== switcher) s.classList.remove('open');
        });
        switcher.classList.toggle('open');
        const isExpanded = switcher.classList.contains('open');
        btn.setAttribute('aria-expanded', isExpanded);
      });
    }
  });

  document.addEventListener('click', (e) => {
    langSwitchers.forEach(s => {
      if (!s.contains(e.target)) {
        s.classList.remove('open');
        const btn = s.querySelector('.lang-btn');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* --------------------------------------------------------------------------
     3. SCROLL REVEAL ANIMATIONS (IntersectionObserver)
     -------------------------------------------------------------------------- */
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && revealElements.length > 0) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.15,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));
  } else {
    revealElements.forEach(el => el.classList.add('active'));
  }

  /* --------------------------------------------------------------------------
     4. ANIMATED STATISTIC COUNTERS
     -------------------------------------------------------------------------- */
  const counterElements = document.querySelectorAll('.stat-number');

  if ('IntersectionObserver' in window && counterElements.length > 0) {
    const counterObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.getAttribute('data-target') || el.innerText.replace(/[^0-9]/g, ''), 10);
          const suffix = el.getAttribute('data-suffix') || '+';
          const prefix = el.getAttribute('data-prefix') || '';
          const duration = 2000;
          const frameRate = 30;
          const totalFrames = Math.round(duration / (1000 / frameRate));
          let frame = 0;

          if (!isNaN(target)) {
            const counterInterval = setInterval(() => {
              frame++;
              const currentProgress = frame / totalFrames;
              const easeOutProgress = 1 - Math.pow(1 - currentProgress, 3);
              const currentCount = Math.round(easeOutProgress * target);

              el.innerText = `${prefix}${currentCount.toLocaleString()}${suffix}`;

              if (frame >= totalFrames) {
                clearInterval(counterInterval);
                el.innerText = `${prefix}${target.toLocaleString()}${suffix}`;
              }
            }, 1000 / frameRate);
          }

          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });

    counterElements.forEach(el => counterObserver.observe(el));
  }

  /* --------------------------------------------------------------------------
     5. HERO SEARCH BAR TABS & FORM
     -------------------------------------------------------------------------- */
  const searchTabBtns = document.querySelectorAll('.search-tab-btn');
  const searchForm = document.querySelector('.search-form');

  if (searchTabBtns.length > 0) {
    searchTabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        searchTabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const type = btn.getAttribute('data-type');
        const i18n = window.I18N_STRINGS || {};
        if (type === 'flight') {
          showToast(i18n.search_flight_mode || 'Uçuş axtarış rejimi aktivləşdirildi ✈️', 'info');
        } else if (type === 'hotel') {
          showToast(i18n.search_hotel_mode || 'Otel və rezort axtarış rejimi aktivləşdirildi 🏨', 'info');
        } else {
          showToast(i18n.search_tour_mode || 'Tur paketləri axtarış rejimi aktivləşdirildi 🌍', 'info');
        }
      });
    });
  }

  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const destination = searchForm.querySelector('input[name="destination"]')?.value || 'İstiqamət';
      const guests = searchForm.querySelector('select[name="guests"]')?.value || '1';
      const i18n = window.I18N_STRINGS || {};
      const searchMsg = i18n.search_searching || 'Axtarış icra edilir...';
      
      showToast(`${searchMsg} (${destination})`, 'success');
      setTimeout(() => {
        window.location.href = '/services/';
      }, 800);
    });
  }

  /* --------------------------------------------------------------------------
     6. CATEGORY FILTERING (SERVICES & BLOG)
     -------------------------------------------------------------------------- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const filterItems = document.querySelectorAll('.filterable-item');

  if (filterBtns.length > 0 && filterItems.length > 0) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filterValue = btn.getAttribute('data-filter');

        filterItems.forEach(item => {
          const category = item.getAttribute('data-category');
          if (filterValue === 'all' || category === filterValue || category?.includes(filterValue)) {
            item.style.display = 'flex';
            setTimeout(() => {
              item.style.opacity = '1';
              item.style.transform = 'scale(1)';
            }, 50);
          } else {
            item.style.opacity = '0';
            item.style.transform = 'scale(0.95)';
            setTimeout(() => {
              item.style.display = 'none';
            }, 300);
          }
        });
      });
    });
  }

  /* --------------------------------------------------------------------------
     7. TOUR GALLERY SWITCHER (SERVICE-SINGLE)
     -------------------------------------------------------------------------- */
  const mainGalleryImg = document.querySelector('.tour-gallery-main img');
  const thumbGalleryImgs = document.querySelectorAll('.tour-gallery-thumb');

  if (mainGalleryImg && thumbGalleryImgs.length > 0) {
    thumbGalleryImgs.forEach(thumb => {
      thumb.addEventListener('click', () => {
        thumbGalleryImgs.forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
        const newSrc = thumb.querySelector('img').getAttribute('src');
        
        mainGalleryImg.style.opacity = '0.3';
        setTimeout(() => {
          mainGalleryImg.setAttribute('src', newSrc);
          mainGalleryImg.style.opacity = '1';
        }, 200);
      });
    });
  }

  /* --------------------------------------------------------------------------
     8. DAY-BY-DAY ITINERARY ACCORDION (SERVICE-SINGLE)
     -------------------------------------------------------------------------- */
  const itineraryHeaders = document.querySelectorAll('.itinerary-header');

  if (itineraryHeaders.length > 0) {
    itineraryHeaders.forEach(header => {
      header.addEventListener('click', () => {
        const parentItem = header.parentElement;
        const isActive = parentItem.classList.contains('active');

        // Toggle clicked item
        if (isActive) {
          parentItem.classList.remove('active');
        } else {
          parentItem.classList.add('active');
        }
      });
    });
  }

  /* --------------------------------------------------------------------------
     9. TOUR LIVE BOOKING CALCULATOR
     -------------------------------------------------------------------------- */
  const guestSelect = document.querySelector('#booking-guests');
  const packageTypeSelect = document.querySelector('#booking-package-type');
  const basePricePerPerson = 1290; // Default base price in AZN

  function updateBookingPrice() {
    const guests = parseInt(guestSelect?.value || '1', 10);
    const multiplier = parseFloat(packageTypeSelect?.value || '1.0');
    const pricePerPerson = Math.round(basePricePerPerson * multiplier);
    const subtotal = pricePerPerson * guests;
    const taxes = Math.round(subtotal * 0.05); // 5% service fee/tax
    const total = subtotal + taxes;

    const baseEl = document.querySelector('#calc-base-price');
    const taxEl = document.querySelector('#calc-tax-price');
    const totalEl = document.querySelector('#calc-total-price');

    if (baseEl) baseEl.innerText = `${subtotal.toLocaleString()} ₼`;
    if (taxEl) taxEl.innerText = `${taxes.toLocaleString()} ₼`;
    if (totalEl) totalEl.innerText = `${total.toLocaleString()} ₼`;
  }

  if (guestSelect) guestSelect.addEventListener('change', updateBookingPrice);
  if (packageTypeSelect) packageTypeSelect.addEventListener('change', updateBookingPrice);

  /* --------------------------------------------------------------------------
     10. BOOKING MODAL & INTERACTION
     -------------------------------------------------------------------------- */
  const modalOverlay = document.querySelector('.modal-overlay');
  const modalCloseBtn = document.querySelector('.modal-close-btn');
  const openModalBtns = document.querySelectorAll('.open-booking-modal');
  const modalTourName = document.querySelector('#modal-tour-name');

  if (modalOverlay) {
    openModalBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const tourTitle = btn.getAttribute('data-tour') || 'Seçilmiş Tur Paketi';
        if (modalTourName) modalTourName.innerText = tourTitle;
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    if (modalCloseBtn) {
      modalCloseBtn.addEventListener('click', () => {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
      });
    }

    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
      }
    });

    const modalForm = document.querySelector('#modal-booking-form');
    if (modalForm) {
      modalForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const i18n = window.I18N_STRINGS || {};
        
        const formData = new FormData(modalForm);
        const selectedTourEl = document.querySelector('#modal-tour-name');
        if (selectedTourEl) {
          formData.append('tour', selectedTourEl.textContent.trim());
        }

        fetch('/api/book-tour/', {
          method: 'POST',
          body: formData
        }).then(res => res.json()).catch(err => console.error('Booking request error:', err));

        showToast(i18n.booking_success || 'Təşəkkür edirik! Rezervasiya sorğunuz qəbul edildi. Menecerimiz 15 dəqiqə ərzində sizinlə əlaqə saxlayacaq.', 'success');
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        modalForm.reset();
      });
    }
  }

  /* --------------------------------------------------------------------------
     11. CONTACT & NEWSLETTER FORMS
     -------------------------------------------------------------------------- */
  const contactForm = document.querySelector('#contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const i18n = window.I18N_STRINGS || {};
      const formData = new FormData(contactForm);
      formData.append('ajax', '1');

      fetch('/contact/', {
        method: 'POST',
        body: formData
      }).then(res => res.json()).catch(err => console.error('Contact submit error:', err));

      showToast(i18n.contact_success || 'Təşəkkür edirik! Mesajınız uğurla göndərildi. Tezliklə cavablandırılacaq.', 'success');
      contactForm.reset();
    });
  }

  const newsletterForms = document.querySelectorAll('.newsletter-form');
  newsletterForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const i18n = window.I18N_STRINGS || {};
      const emailInput = form.querySelector('input[type="email"]');
      if (emailInput && emailInput.value.trim() !== '') {
        const formData = new FormData(form);
        fetch('/api/subscribe-newsletter/', {
          method: 'POST',
          body: formData
        }).then(res => res.json()).catch(err => console.error('Newsletter error:', err));

        showToast(i18n.newsletter_success || 'Təbrik edirik! VIP səyahət təkliflərinə uğurla abunə oldunuz 🎁', 'success');
        form.reset();
      } else {
        showToast(i18n.newsletter_invalid || 'Zəhmət olmasa düzgün e-poçt ünvanı daxil edin.', 'error');
      }
    });
  });

  const commentForm = document.querySelector('#comment-form');
  if (commentForm) {
    commentForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const i18n = window.I18N_STRINGS || {};
      showToast(i18n.comment_success || 'Şərhiniz üçün təşəkkürlər! Yoxlanışdan sonra dərc ediləcək.', 'success');
      commentForm.reset();
    });
  }

  /* --------------------------------------------------------------------------
     12. COPY SHARE LINK
     -------------------------------------------------------------------------- */
  const copyLinkBtn = document.querySelector('#copy-link-btn');
  if (copyLinkBtn) {
    copyLinkBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const i18n = window.I18N_STRINGS || {};
      navigator.clipboard.writeText(window.location.href).then(() => {
        showToast(i18n.link_copied || 'Məqalənin linki kopyalandı! 📋', 'success');
      }).catch(() => {
        showToast(i18n.link_copy_failed || 'Link kopyalana bilmədi.', 'error');
      });
    });
  }

  /* --------------------------------------------------------------------------
     13. TOAST NOTIFICATION UTILITY
     -------------------------------------------------------------------------- */
  window.showToast = function(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';

    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(50px)';
      toast.style.transition = 'all 0.3s ease-out';
      setTimeout(() => {
        if (toast.parentElement) {
          toast.remove();
        }
      }, 300);
    }, 3800);
  };

  /* --------------------------------------------------------------------------
     14. CINEMATIC PARALLAX PAGE TRANSITION & SCROLL ENGINE
     -------------------------------------------------------------------------- */
  // 14.1 Inject Parallax Overlay dynamically if not present
  let parallaxOverlay = document.querySelector('.parallax-transition-overlay');
  if (!parallaxOverlay) {
    parallaxOverlay = document.createElement('div');
    parallaxOverlay.className = 'parallax-transition-overlay';
    parallaxOverlay.id = 'parallax-transition-overlay';
    parallaxOverlay.innerHTML = `
      <div class="parallax-layer parallax-layer-1"></div>
      <div class="parallax-layer parallax-layer-2"></div>
      <div class="parallax-transition-content">
        <div class="parallax-brand-icon">
          <i class="fas fa-compass"></i>
        </div>
        <div class="parallax-brand-text">
          TRAVELISTIC <span>2026</span>
        </div>
      </div>
    `;
    document.body.prepend(parallaxOverlay);
  }

  // 14.2 Incoming Page Parallax Reveal
  const wasNavigated = sessionStorage.getItem('travelistic_nav');
  if (wasNavigated) {
    sessionStorage.removeItem('travelistic_nav');
    document.body.classList.add('parallax-page-revealing');
    setTimeout(() => {
      document.body.classList.remove('parallax-page-revealing');
    }, 700);
  }

  // Initial body smooth float-in
  document.body.classList.add('page-enter-active');

  // 14.3 Intercept page navigation for Parallax Transition
  let isNavigating = false;
  const pageLinks = document.querySelectorAll('a[href]');

  pageLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');

      // Skip non-page links
      if (!href) return;
      if (href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('tel:') || href.startsWith('mailto:')) return;
      if (link.hasAttribute('download') || link.getAttribute('target') === '_blank') return;
      if (link.classList.contains('open-booking-modal') || link.closest('.open-booking-modal')) return;

      // Check if it's an internal link
      const targetUrl = new URL(link.href, window.location.href);
      if (targetUrl.origin !== window.location.origin) return;

      // If linking to the exact same page, let browser or smooth scroll handle it
      if (targetUrl.pathname === window.location.pathname && targetUrl.search === window.location.search && targetUrl.hash) {
        return;
      }

      // Trigger Parallax Transition
      e.preventDefault();
      if (isNavigating) return;
      isNavigating = true;

      sessionStorage.setItem('travelistic_nav', '1');
      document.body.classList.add('parallax-transitioning');

      // Wait for dual-layer parallax sweep before navigating
      setTimeout(() => {
        window.location.href = link.href;
      }, 480);
    });
  });

  // Handle browser Back/Forward (BFCache)
  window.addEventListener('pageshow', () => {
    isNavigating = false;
    document.body.classList.remove('parallax-transitioning');
  });

  // 14.4 Smooth Scroll Parallax for Hero & Page Banners
  const parallaxBanners = document.querySelectorAll('.hero, .page-banner');
  let tickingScroll = false;

  function updateScrollParallax() {
    const scrollY = window.scrollY;
    parallaxBanners.forEach(banner => {
      const rect = banner.getBoundingClientRect();
      if (rect.bottom > 0 && rect.top < window.innerHeight) {
        const offset = (scrollY - banner.offsetTop) * 0.35;
        banner.style.backgroundPositionY = `calc(50% + ${offset}px)`;
      }
    });
    tickingScroll = false;
  }

  if (parallaxBanners.length > 0) {
    window.addEventListener('scroll', () => {
      if (!tickingScroll) {
        window.requestAnimationFrame(updateScrollParallax);
        tickingScroll = true;
      }
    }, { passive: true });
    updateScrollParallax();
  }

  // 14.5 Interactive 3D Parallax Tilt on Hero Content (Desktop)
  const heroElement = document.querySelector('.hero');
  const heroContent = document.querySelector('.hero-content');
  if (heroElement && heroContent) {
    heroElement.addEventListener('mousemove', (e) => {
      if (window.innerWidth < 992) return;
      const rect = heroElement.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

      heroContent.style.transform = `perspective(1000px) rotateY(${x * 4}deg) rotateX(${-y * 4}deg) translateY(${y * -5}px)`;
    });

    heroElement.addEventListener('mouseleave', () => {
      heroContent.style.transform = 'none';
      heroContent.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
    });

    heroElement.addEventListener('mouseenter', () => {
      heroContent.style.transition = 'transform 0.1s ease-out';
    });
  }
});


