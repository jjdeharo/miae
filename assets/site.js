(() => {
  const supported = ['es', 'ca', 'eu', 'gl', 'en'];
  const key = 'miae-language';
  const body = document.body;
  const root = new URL(body.dataset.root || './', window.location.href);
  const browserLanguage = () => {
    for (const locale of navigator.languages || [navigator.language]) {
      const code = locale.toLowerCase().split(/[-_]/)[0];
      if (supported.includes(code)) return code;
    }
    return 'es';
  };
  let saved;
  try { saved = localStorage.getItem(key); } catch (_) { /* Storage may be disabled. */ }
  const preferred = supported.includes(saved) ? saved : browserLanguage();
  const paths = {document: (lang) => `v2.1/${lang}/`, tools: (lang) => `${lang}/ficha/`,
                 quickref: (lang) => `${lang}/guia/`};
  const destination = (lang) => {
    const path = (paths[body.dataset.page] || ((code) => `${code}/`))(lang);
    const url = new URL(path, root);
    url.search = window.location.search;
    url.hash = window.location.hash;
    return url;
  };
  // Explicit language URLs remain shareable; only neutral entry points redirect.
  if (body.hasAttribute('data-auto-language')) {
    window.location.replace(destination(preferred).href);
    return;
  }
  const selector = document.querySelector('[data-language-select]');
  if (!selector) return;
  if (saved === 'auto' && document.documentElement.lang === preferred) selector.value = 'auto';
  selector.addEventListener('change', () => {
    const choice = selector.value;
    if (choice !== 'auto' && !supported.includes(choice)) return;
    try { localStorage.setItem(key, choice); } catch (_) { /* Navigation still works. */ }
    window.location.assign(destination(choice === 'auto' ? browserLanguage() : choice).href);
  });
})();

(() => {
  const controls = document.querySelector('[data-zoom]');
  if (!controls || !CSS.supports('zoom', '1.5')) return;
  const steps = [0.6, 0.7, 0.8, 0.9, 1, 1.15, 1.3, 1.5, 1.75, 2];
  const key = 'miae-quickref-zoom';
  const value = controls.querySelector('[data-zoom-reset]');
  const buttons = controls.querySelectorAll('[data-zoom-step]');
  let index = steps.indexOf(1);
  let stored;
  try { stored = Number(localStorage.getItem(key)); } catch (_) { /* Storage may be disabled. */ }
  if (steps.includes(stored)) index = steps.indexOf(stored);
  const apply = (remember) => {
    const level = steps[index];
    document.documentElement.style.setProperty('--qr-zoom', level);
    value.textContent = `${Math.round(level * 100)}\u00a0%`;
    buttons.forEach((button) => {
      const next = index + Number(button.dataset.zoomStep);
      button.disabled = next < 0 || next >= steps.length;
    });
    if (remember) { try { localStorage.setItem(key, level); } catch (_) { /* Zoom still applies. */ } }
  };
  buttons.forEach((button) => button.addEventListener('click', () => {
    const next = index + Number(button.dataset.zoomStep);
    if (next < 0 || next >= steps.length) return;
    index = next;
    apply(true);
  }));
  value.addEventListener('click', () => { index = steps.indexOf(1); apply(true); });
  controls.hidden = false;
  apply(false);
})();
