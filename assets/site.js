(() => {
  const selector = document.querySelector('[data-language-select]');
  if (!selector) return;
  selector.addEventListener('change', () => {
    window.location.href = `../${selector.value}/`;
  });
})();
