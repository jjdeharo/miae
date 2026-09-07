(() => {
  document.querySelectorAll('[data-editor]').forEach(editor => {
    const field = editor.querySelector('textarea');
    const status = editor.querySelector('[role="status"]');
    editor.querySelector('[data-copy]').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(field.value);
        status.textContent = editor.dataset.copied;
      } catch (_) {
        field.focus();
        field.select();
        status.textContent = editor.dataset.copyFailed;
      }
    });
    editor.querySelector('[data-download]').addEventListener('click', event => {
      const url = URL.createObjectURL(new Blob([field.value], {type: 'text/plain;charset=utf-8'}));
      const link = document.createElement('a');
      link.href = url;
      link.download = event.currentTarget.dataset.download;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    editor.classList.add('interactive-ready');
  });
})();
