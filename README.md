# MIAE

Edición web y descargable del Marco para la integración de la IA generativa
en las tareas educativas, de Juan José de Haro.

La versión vigente es la 2.1 y se ofrece en castellano, catalán, euskera,
gallego e inglés. Cada versión conserva una URL propia y permanente.

## Construcción

```bash
python3 scripts/build.py --pdf
python3 scripts/validate.py
```

El script genera la portada, las páginas de cada idioma y los PDF de
`output/pdf/` a partir de los Markdown de `content/`. Los archivos de
`v2-revisada/` son históricos y no se regeneran.

## Licencia

[Creative Commons Reconocimiento-CompartirIgual 4.0 Internacional](LICENSE).

## Idioma de la web

La entrada `/` y `/v2.1/` eligen el primer idioma compatible de las
preferencias del navegador (es, ca, eu, gl o en), con castellano como alternativa.
El selector permite guardar una elección manual en este navegador o volver a
«Automático». Las portadas `/<idioma>/` y los documentos `/v2.1/<idioma>/`
conservan su idioma cuando se abren mediante un enlace directo. La navegación
entre portada, documento y PDF mantiene el idioma actual.

Las traducciones de la portada están en `data/home-ui.json`; las del resto de
la interfaz, en `scripts/build.py`. Los recursos externos y la edición histórica
conservan su idioma original, indicado en los enlaces correspondientes.

La lógica de selección se comprueba con `node scripts/test-language.cjs`.
