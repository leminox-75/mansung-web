/**
 * 만성코프레이션 공통 JavaScript
 * 헤더 스크롤 효과, 모바일 메뉴, 히어로 슬라이더, 공지사항 로드 등
 */

/* ── 헤더 스크롤 효과 ──────────────────────────────────────── */
(function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      header.style.boxShadow = '0 2px 20px rgba(0,0,0,.15)';
    } else {
      header.style.boxShadow = '0 2px 8px rgba(0,0,0,.08)';
    }
  });
})();

/* ── 모바일 메뉴 (드로어) ──────────────────────────────────── */
(function initMobileMenu() {
  const hamburger   = document.querySelector('.hamburger');
  const mobileNav   = document.querySelector('.mobile-nav');
  const overlay     = document.querySelector('.mobile-overlay');
  const closeBtn    = document.querySelector('.mobile-nav-close');

  if (!hamburger) return;

  /**
   * 모바일 메뉴 열기
   */
  function openMenu() {
    mobileNav.classList.add('open');
    mobileNav.style.display = 'block';
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  /**
   * 모바일 메뉴 닫기
   */
  function closeMenu() {
    mobileNav.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  hamburger.addEventListener('click', openMenu);
  closeBtn && closeBtn.addEventListener('click', closeMenu);
  overlay  && overlay.addEventListener('click', closeMenu);

  // 모바일 서브메뉴 토글
  document.querySelectorAll('.m-menu-title').forEach(title => {
    title.addEventListener('click', () => {
      const sub = title.nextElementSibling;
      if (sub && sub.classList.contains('m-sub-menu')) {
        sub.classList.toggle('open');
      }
    });
  });
})();

/* ── 히어로 슬라이더 ─────────────────────────────────────── */
(function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots   = document.querySelectorAll('.hero-dot');
  if (!slides.length) return;

  let current   = 0;
  let timer     = null;
  const INTERVAL = 5000;

  /**
   * 지정 인덱스 슬라이드로 전환
   * @param {number} idx - 이동할 슬라이드 인덱스
   */
  function goTo(idx) {
    slides[current].classList.remove('active');
    dots[current] && dots[current].classList.remove('active');
    current = (idx + slides.length) % slides.length;
    slides[current].classList.add('active');
    dots[current] && dots[current].classList.add('active');
  }

  /** 자동 재생 시작 */
  function startAuto() {
    timer = setInterval(() => goTo(current + 1), INTERVAL);
  }

  /** 자동 재생 정지 */
  function stopAuto() {
    clearInterval(timer);
  }

  // 도트 클릭
  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => { stopAuto(); goTo(i); startAuto(); });
  });

  // 화살표 클릭
  const prevBtn = document.querySelector('.hero-arrow.prev');
  const nextBtn = document.querySelector('.hero-arrow.next');
  prevBtn && prevBtn.addEventListener('click', () => { stopAuto(); goTo(current - 1); startAuto(); });
  nextBtn && nextBtn.addEventListener('click', () => { stopAuto(); goTo(current + 1); startAuto(); });

  startAuto();
})();

/* ── 공지사항 로드 ─────────────────────────────────────────── */
(function initNoticeList() {
  const listEl = document.querySelector('.notice-api-list');
  if (!listEl) return;

  /**
   * API에서 공지사항을 가져와 목록을 렌더링
   * DB 미연결 시 기본 데이터로 폴백
   */
  async function loadNotices() {
    try {
      const res  = await fetch('/api/notices/?limit=5');
      const data = await res.json();
      renderNotices(data);
    } catch {
      // API 미연결 시 샘플 데이터 표시
      renderNotices([
        { id: 1, title: '2024년 신제품 비닐하우스 자재 출시 안내', created_at: '2024-12-01', category: '공지' },
        { id: 2, title: '겨울철 비닐하우스 설치 할인 이벤트',       created_at: '2024-11-20', category: '이벤트' },
        { id: 3, title: '회사 창립 30주년 기념 고객 감사 행사',      created_at: '2024-11-10', category: '뉴스' },
        { id: 4, title: '프레스 제품 품질인증 취득 알림',            created_at: '2024-10-28', category: '공지' },
        { id: 5, title: '연말 정기 점검 공지',                       created_at: '2024-10-15', category: '공지' },
      ]);
    }
  }

  /**
   * 공지사항 목록 HTML 렌더링
   * @param {Array} items - 공지사항 배열
   */
  function renderNotices(items) {
    listEl.innerHTML = items.map(item => {
      const date = item.created_at.slice(0, 10).replace(/-/g, '.');
      return `
        <li>
          <span class="badge badge-primary">${item.category || '공지'}</span>
          <a href="/support/notices?id=${item.id}" class="n-title">${item.title}</a>
          <span class="n-date">${date}</span>
        </li>`;
    }).join('');
  }

  loadNotices();
})();

/* ── 제품 탭 필터 ─────────────────────────────────────────── */
(function initProductTabs() {
  const tabs  = document.querySelectorAll('.tab-btn');
  const cards = document.querySelectorAll('.product-card');
  if (!tabs.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.dataset.filter;
      cards.forEach(card => {
        if (filter === 'all' || card.dataset.category === filter) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
})();

/* ── 카운터 애니메이션 ─────────────────────────────────────── */
(function initCounterAnimation() {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;

      const el     = entry.target;
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || '';
      let current  = 0;
      const step   = Math.ceil(target / 60);

      /**
       * 숫자를 목표값까지 점진적으로 증가시키는 타이머
       */
      const timer = setInterval(() => {
        current += step;
        if (current >= target) {
          current = target;
          clearInterval(timer);
        }
        el.textContent = current.toLocaleString() + suffix;
      }, 20);

      observer.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => observer.observe(el));
})();

/* ── 문의 폼 제출 ─────────────────────────────────────────── */
(function initContactForm() {
  const form = document.querySelector('#contact-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = form.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = '전송 중...';

    const data = {
      name:    form.name.value,
      company: form.company.value,
      phone:   form.phone.value,
      email:   form.email.value,
      product: form.product?.value || '',
      message: form.message.value,
    };

    try {
      const res = await fetch('/api/contact/', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(data),
      });

      if (res.ok) {
        showToast('문의가 접수되었습니다. 빠른 시일 내 답변드리겠습니다.', 'success');
        form.reset();
      } else {
        showToast('접수 중 오류가 발생했습니다. 다시 시도해 주세요.', 'error');
      }
    } catch {
      showToast('서버 연결에 실패했습니다. 전화로 문의해 주세요.', 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = '문의 접수';
    }
  });
})();

/* ── 토스트 알림 ──────────────────────────────────────────── */
/**
 * 화면 우하단에 토스트 메시지를 표시
 * @param {string} msg  - 표시할 메시지
 * @param {string} type - 'success' | 'error'
 */
function showToast(msg, type = 'success') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = msg;
  toast.style.cssText = `
    position: fixed; bottom: 32px; right: 32px; z-index: 9999;
    padding: 14px 24px; border-radius: 8px; font-size: .875rem; font-weight: 600;
    background: ${type === 'success' ? '#1B6B3A' : '#c0392b'}; color: #fff;
    box-shadow: 0 4px 20px rgba(0,0,0,.2);
    animation: slideUp .3s ease;
  `;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

/* ── 스크롤 상단 이동 버튼 ─────────────────────────────────── */
(function initScrollTop() {
  const btn = document.createElement('button');
  btn.innerHTML = '▲';
  btn.title = '맨 위로';
  btn.style.cssText = `
    position: fixed; bottom: 32px; right: 32px; z-index: 500;
    width: 44px; height: 44px; border-radius: 50%;
    background: var(--primary); color: #fff;
    font-size: .9rem; box-shadow: 0 4px 16px rgba(0,0,0,.2);
    transition: opacity .3s, transform .3s;
    opacity: 0; pointer-events: none;
  `;
  document.body.appendChild(btn);

  window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
    } else {
      btn.style.opacity = '0';
      btn.style.pointerEvents = 'none';
    }
  });

  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();
