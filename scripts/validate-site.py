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
    for key in ('steps', 'fields', 'filled', 'teacher_fields'):
        assert len(guide[key]) == len(reference[key]), f'{lang}: incomplete {key}'
    for path in (ROOT / lang / 'index.html', ROOT / lang / 'ficha' / 'index.html',
                 ROOT / lang / 'guia' / 'index.html', ROOT / 'v2.1' / lang / 'index.html'):
        soup = page(path)
        assert soup.html['lang'] == lang
        # The quick guide is a standalone printable sheet and carries its own colophon.
        if not soup.select('.sheet'):
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
    assert len(home.select('.level-spectrum a')) == 6
    # The homepage is description plus access: no forms, no quiz.
    assert not home.select('[data-editor]') and not home.select('form')
    assert home.select_one(f'.resource-grid a[href="../{lang}/ficha/"]')
    assert home.select_one(f'.resource-grid a[href="../{lang}/guia/"]')
    quickref = page(ROOT / lang / 'guia' / 'index.html')
    assert len(quickref.select('.level')) == 6, f'{lang}: quick guide levels'
    assert len(quickref.select('.rule')) == 5, f'{lang}: quick guide rules'
    assert len(quickref.select('.sheet')) == 2, f'{lang}: quick guide sheets'
    tools = page(ROOT / lang / 'ficha' / 'index.html')
    assert len(tools.select('[data-editor]')) == 2
    for editor in tools.select('[data-editor]'):
        assert editor.select_one('[data-copy]').text == guide['copy']
        assert editor.select_one('textarea').text.strip()
    document = page(ROOT / 'v2.1' / lang / 'index.html')
    assert document.select_one('.mobile-index a[href="#clasificar"]')
    assert document.select_one('.mobile-index a[href="#resumen"]')
print('Validated five complete guides, twenty localized pages, forms and internal links/anchors.')
