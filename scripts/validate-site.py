#!/usr/bin/env python3
"""Check localized guide completeness, rendered controls and internal navigation."""
import json
from pathlib import Path
from urllib.parse import unquote, urlparse
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('es', 'ca', 'eu', 'gl', 'en')
reference = json.loads((ROOT / 'data/guide/es.json').read_text())
cache = {}

def page(path):
    if path not in cache:
        cache[path] = BeautifulSoup(path.read_text(), 'html.parser')
    return cache[path]

for lang in LANGUAGES:
    guide = json.loads((ROOT / f'data/guide/{lang}.json').read_text())
    assert guide.keys() == reference.keys(), f'{lang}: missing translated fields'
    for key in ('steps', 'examples', 'fields', 'filled', 'teacher_fields', 'faqs', 'cases', 'changes'):
        assert len(guide[key]) == len(reference[key]), f'{lang}: incomplete {key}'
    assert [case['correct'] for case in guide['cases']] == ['1', '5', '4', 'mixed']
    for path in (ROOT / lang / 'index.html', ROOT / 'v2.1' / lang / 'index.html'):
        soup = page(path)
        assert soup.html['lang'] == lang
        assert soup.select('footer a')[-1]['href'] == 'https://educacion.bilateria.org/marco-para-la-integracion-de-la-ia-generativa-en-las-tareas-educativas-v-2-revisada'
        ids = [element['id'] for element in soup.select('[id]')]
        assert len(ids) == len(set(ids)), f'{path}: duplicate IDs'
        assert 'built-in method' not in str(soup), f'{path}: template attribute collision'
        for element in soup.select('a[href], script[src], link[href]'):
            target = urlparse(element.get('href', element.get('src')))
            if target.scheme or target.netloc:
                continue
            resolved = (path.parent / unquote(target.path)).resolve() if target.path else path
            if resolved.is_dir():
                resolved /= 'index.html'
            assert resolved.exists(), f'{path}: broken path {target.geturl()}'
            if target.fragment and resolved.suffix == '.html':
                assert page(resolved).find(id=unquote(target.fragment)), f'{path}: broken anchor {target.geturl()}'
    home = page(ROOT / lang / 'index.html')
    assert len(home.select('.comparison-row')) == 6
    assert len(home.select('[data-case]')) == 4
    assert len(home.select('[data-editor]')) == 2
    for editor in home.select('[data-editor]'):
        assert editor.select_one('[data-copy]').text == guide['copy']
        assert editor.select_one('textarea').text.strip()
    for case in home.select('[data-case]'):
        assert len(case.select('input[type=radio]')) == 7
        assert case.select_one(f'input[value="{case["data-answer"]}"]')
        assert case.select_one('[role=status]')
        assert case.select_one('.no-interaction p').text == case['data-explanation']
    document = page(ROOT / 'v2.1' / lang / 'index.html')
    assert document.select_one('.mobile-index a[href="#clasificar"]')
    assert document.select_one('.mobile-index a[href="#resumen"]')
print('Validated five complete guides, ten localized pages, forms and internal links/anchors.')
