/* HouseSquare — Main JS */

// ─── NAVBAR SCROLL ───────────────────────────────────────────
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.style.boxShadow = window.scrollY > 40
      ? '0 4px 24px rgba(30,30,30,0.10)'
      : 'none';
  });
}

// ─── HAMBURGER MENU ──────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    const spans = hamburger.querySelectorAll('span');
    const isOpen = navLinks.classList.contains('open');
    spans[0].style.transform = isOpen ? 'rotate(45deg) translate(5px,6px)' : '';
    spans[1].style.opacity   = isOpen ? '0' : '1';
    spans[2].style.transform = isOpen ? 'rotate(-45deg) translate(5px,-6px)' : '';
  });
}

// ─── FILTER BHK ACTIVE STATE ─────────────────────────────────
document.querySelectorAll('.bhk-opt input').forEach(radio => {
  radio.addEventListener('change', () => {
    document.querySelectorAll('.bhk-opt').forEach(l => l.classList.remove('active'));
    if (radio.checked) radio.closest('.bhk-opt').classList.add('active');
  });
});

// ─── CARD FAV TOGGLE ─────────────────────────────────────────
document.querySelectorAll('.card-fav').forEach(btn => {
  btn.addEventListener('click', e => {
    e.preventDefault();
    const liked = btn.textContent.trim() === '❤';
    btn.textContent = liked ? '♡' : '❤';
    btn.style.transform = 'scale(1.3)';
    setTimeout(() => { btn.style.transform = ''; }, 200);
  });
});

// ─── SCROLL REVEAL ───────────────────────────────────────────
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.listing-card, .step, .agent-card, .agent-full-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// ─── FILTER FORM: MAINTAIN SCROLL ────────────────────────────
const filterForm = document.getElementById('filterForm');
if (filterForm) {
  filterForm.querySelectorAll('select').forEach(sel => {
    sel.addEventListener('change', () => filterForm.submit());
  });
}

// ─── PRICE FORMATTER IN ENLIST FORM ──────────────────────────
const priceInput = document.querySelector('input[name="price"]');
if (priceInput) {
  priceInput.addEventListener('blur', () => {
    const val = parseFloat(priceInput.value.replace(/,/g, ''));
    if (!isNaN(val)) {
      let label = '';
      if (val >= 10_000_000) label = `≈ ₹${(val/10_000_000).toFixed(2)} Cr`;
      else if (val >= 100_000) label = `≈ ₹${(val/100_000).toFixed(2)} L`;
      let hint = priceInput.parentElement.querySelector('.price-hint');
      if (!hint) {
        hint = document.createElement('span');
        hint.className = 'price-hint';
        hint.style.cssText = 'font-size:12px;color:var(--terracotta);margin-top:4px;display:block;';
        priceInput.parentElement.appendChild(hint);
      }
      hint.textContent = label;
    }
  });
}

// ─── AUTO DISMISS ALERTS ─────────────────────────────────────
document.querySelectorAll('.alert').forEach(alert => {
  setTimeout(() => {
    alert.style.opacity = '0';
    alert.style.transform = 'translateX(100%)';
    alert.style.transition = 'all 0.4s ease';
    setTimeout(() => alert.remove(), 400);
  }, 5000);
});
