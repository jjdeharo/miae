const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('assets/site.js', 'utf8');
function run({languages = ['es'], saved, automatic = true, page = 'home', lang = 'es', blocked = false, choice, href = 'https://example.org/miae/', root = './'} = {}) {
  let navigated, handler;
  const selector = {value: lang, addEventListener: (_, callback) => { handler = callback; }};
  const context = {
    URL, navigator: {languages},
    localStorage: {getItem: () => { if (blocked) throw Error(); return saved; }, setItem: (_, value) => { if (blocked) throw Error(); saved = value; }},
    document: {body: {dataset: {page, root}, hasAttribute: () => automatic}, documentElement: {lang}, querySelector: () => selector},
    window: {location: {href, search: new URL(href).search, hash: new URL(href).hash, replace: url => {navigated = url;}, assign: url => {navigated = url;}}}
  };
  vm.runInNewContext(source, context);
  if (choice) { selector.value = choice; handler(); }
  return {navigated, saved};
}
assert.equal(run({languages:['ca-ES','es']}).navigated, 'https://example.org/miae/ca/');
assert.equal(run({languages:['fr','gl-ES','en']}).navigated, 'https://example.org/miae/gl/');
assert.equal(run({languages:['de']}).navigated, 'https://example.org/miae/es/');
assert.equal(run({languages:['en-US'],saved:'eu'}).navigated, 'https://example.org/miae/eu/');
assert.equal(run({languages:['en'],saved:'invalid'}).navigated, 'https://example.org/miae/en/');
assert.equal(run({languages:['gl'],blocked:true}).navigated, 'https://example.org/miae/gl/');
assert.equal(run({automatic:false,saved:'ca'}).navigated, undefined);
const documentOptions = {automatic:false,page:'document',href:'https://example.org/miae/v2.1/es/?ref=test#nivel-4',root:'../../'};
assert.deepEqual(run({...documentOptions,choice:'en'}), {navigated:'https://example.org/miae/v2.1/en/?ref=test#nivel-4',saved:'en'});
assert.equal(run({...documentOptions,choice:'auto',languages:['eu-ES'],saved:'en'}).navigated, 'https://example.org/miae/v2.1/eu/?ref=test#nivel-4');
assert.equal(run({...documentOptions,choice:'ca',blocked:true}).navigated, 'https://example.org/miae/v2.1/ca/?ref=test#nivel-4');
assert.equal(run({page:'document',href:'https://example.org/miae/v2.1/',root:'../',languages:['en']}).navigated, 'https://example.org/miae/v2.1/en/');
console.log('Language routing: 11 checks passed.');
