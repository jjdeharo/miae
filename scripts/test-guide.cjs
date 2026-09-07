const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

(async () => {
  const handlers = {}, result = {textContent: ''};
  const field = {value: 'Tarea: ecosistema\nHipótesis y conclusión — nivel 2.', focus() {this.focused = true;}, select() {this.selected = true;}};
  const button = name => ({addEventListener: (_, handler) => {handlers[name] = handler;}});
  const editor = {
    dataset: {copied: 'Copiado', copyFailed: 'Copiar manualmente'}, classList: {add() {}},
    querySelector: selector => ({'textarea':field, '[role="status"]':result, '[data-copy]':button('copy'), '[data-download]':button('download')})[selector]
  };
  let clipboardText, clipboardBlocked = false, capturedBlob, downloadName, revoked;
  const context = {
    document: {querySelectorAll: selector => selector === '[data-editor]' ? [editor] : [], body: {append() {}}, createElement: () => ({click() {downloadName = this.download;}, remove() {}})},
    navigator: {clipboard: {writeText: async text => {if (clipboardBlocked) throw Error(); clipboardText = text;}}},
    Blob, URL: {createObjectURL: blob => {capturedBlob = blob; return 'blob:download';}, revokeObjectURL: url => {revoked = url;}},
    setTimeout: callback => callback()
  };
  vm.runInNewContext(fs.readFileSync('assets/guide.js', 'utf8'), context);
  await handlers.copy();
  assert.equal(clipboardText, field.value);
  assert.equal(result.textContent, 'Copiado');
  clipboardBlocked = true;
  await handlers.copy();
  assert.equal(result.textContent, 'Copiar manualmente');
  assert.ok(field.focused && field.selected);
  // Download must contain the user's edits, including accents and newlines.
  field.value += '\nEdición posterior: planificación.';
  handlers.download({currentTarget: {dataset: {download: 'miae-ficha-es.txt'}}});
  assert.equal(await capturedBlob.text(), field.value);
  assert.equal(capturedBlob.type, 'text/plain;charset=utf-8');
  assert.equal(downloadName, 'miae-ficha-es.txt');
  assert.equal(revoked, 'blob:download');
  console.log('Guide: copying, clipboard denial and edited UTF-8 download verified.');
})();
