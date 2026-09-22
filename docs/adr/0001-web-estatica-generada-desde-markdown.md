# 1. La web se genera con un script a partir del texto en Markdown, con una URL permanente por versión

Fecha: 2026-09-07 · Estado: aceptado

## Contexto

El MIAE es un texto con versiones sucesivas, publicado en cinco idiomas y
citado desde otras webs y desde Zenodo. Hace falta que cada versión conserve su
dirección, que las cinco ediciones salgan del mismo texto y que el sitio se
pueda alojar en GitHub Pages sin servidor.

## Decisión

El texto canónico de cada idioma vive en `content/v2.1/<idioma>.md`. El script
`scripts/build.py` genera con Jinja la portada, las páginas de cada idioma, la
guía rápida, las fichas y los PDF (con WeasyPrint). Los archivos generados se
suben al repositorio, porque GitHub Pages sirve el resultado tal cual. Cada
versión del marco tiene su carpeta (`v2.1/`) y las anteriores (`v2-revisada/`)
se conservan sin regenerar.

Lo que se muestra más de una vez (los resúmenes de nivel, los anclajes
`#nivel-N`) sale del mismo Markdown, no de una segunda copia que mantener.

## Alternativas descartadas

- Un generador de sitios estándar: añadía dependencias y convenciones para un
  sitio de pocas plantillas, y complicaba producir los PDF desde el mismo HTML.
- Editar el HTML directamente: cinco idiomas y varios formatos habrían
  divergido enseguida.

## Consecuencias

Cualquier cambio de texto se hace en el Markdown y se regenera con
`python3 scripts/build.py` (con `--pdf` cuando cambia el contenido). Los
scripts `validate.py` y `validate-site.py` comprueban que las cinco ediciones
siguen completas y enlazadas.
