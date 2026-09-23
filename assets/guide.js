// Classification sheet: each editable text box has a button to copy its text and another to
// download it as a .txt file. Without JavaScript the text can still be selected by hand.
(() => {
  document.querySelectorAll('[data-editor]').forEach(editor => {
    const field = editor.querySelector('textarea');
    const status = editor.querySelector('[role="status"]');
    editor.querySelector('[data-copy]').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(field.value);
        status.textContent = editor.dataset.copied;
      } catch (_) {
        // Copying failed (permissions, insecure context): select the text so it can be copied by hand.
        field.focus();
        field.select();
        status.textContent = editor.dataset.copyFailed;
      }
    });
    editor.querySelector('[data-download]').addEventListener('click', event => {
      // The file is built in the browser from the current text; nothing is uploaded.
      const url = URL.createObjectURL(new Blob([field.value], {type: 'text/plain;charset=utf-8'}));
      const link = document.createElement('a');
      link.href = url;
      link.download = event.currentTarget.dataset.download;
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
    // Reveals the buttons, which stay hidden until they can work.
    editor.classList.add('interactive-ready');
  });
})();
