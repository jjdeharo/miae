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

// Sharing a level: the control copies a link that opens this level's summary on the home page.
(() => {
  const controls = document.querySelectorAll('[data-share-level]');
  if (!controls.length) return;
  const home = new URL(`${document.documentElement.lang}/`, new URL(document.body.dataset.root || './', window.location.href));
  const copy = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }
    const field = document.createElement('textarea');
    field.value = text;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.append(field);
    field.select();
    const done = document.execCommand('copy');
    field.remove();
    if (!done) throw new Error('copy');
  };
  controls.forEach((control) => {
    const link = control.getAttribute('href') || control.dataset.shareUrl || `${home.href}?nivel=${control.dataset.shareLevel}`;
    const toast = document.createElement('span');
    toast.className = 'share-toast';
    toast.setAttribute('role', 'status');
    control.insertAdjacentElement('afterend', toast);
    let timer;
    control.addEventListener('click', async (event) => {
      event.preventDefault();
      try {
        await copy(link);
        toast.textContent = control.dataset.copied;
      } catch (_) {
        toast.textContent = link;
      }
      toast.classList.add('is-visible');
      clearTimeout(timer);
      timer = setTimeout(() => toast.classList.remove('is-visible'), 2400);
    });
  });
})();

// A shared link (?nivel=N) opens the level summary in a dialog on the home page.
(() => {
  const dialog = document.querySelector('[data-level-dialog]');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const url = new URL(window.location.href);
  const level = url.searchParams.get('nivel');
  const card = /^[0-5]$/.test(level || '') && dialog.querySelector(`[data-level-card="${level}"]`);
  if (!card) return;
  card.hidden = false;
  card.querySelector('h2').id = 'nivel-dialogo-titulo';
  const close = () => dialog.close();
  card.querySelector('[data-level-close]').addEventListener('click', close);
  dialog.addEventListener('click', (event) => { if (event.target === dialog) close(); });
  dialog.addEventListener('close', () => {
    // Closing clears the parameter so a reload or a bookmark shows the plain home page.
    url.searchParams.delete('nivel');
    history.replaceState(null, '', url.href);
  });
  dialog.showModal();
  card.focus({ preventScroll: true });
})();
