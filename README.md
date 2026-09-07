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
la interfaz, en `scripts/build.py`. Los recursos externos conservan su idioma original, indicado en los enlaces
correspondientes. El enlace del pie a la versión anterior abre su artículo en
Bilateria; los archivos históricos se conservan en el repositorio.

La lógica de selección se comprueba con `node scripts/test-language.cjs`.

## Guía práctica

Las portadas incluyen una guía breve, seis procesos comparados para un mismo
informe, fichas editables para declarar el uso de IA y comunicar los usos
permitidos, preguntas frecuentes, cuatro casos con respuesta razonada y las
aclaraciones de la versión 2.1. Los contenidos están en `data/guide/<idioma>.json`
y se generan con `templates/guide.html`. El texto canónico de `content/` se
mantiene como referencia independiente.

Las fichas se copian o descargan como texto en el navegador, sin enviar su
contenido a ningún servicio. Las preguntas frecuentes y las explicaciones de
los ejercicios también son accesibles sin JavaScript. El índice del documento
incluye enlaces estables a la clasificación y al resumen en todos los idiomas,
con una versión desplegable para móviles.

Comprobaciones adicionales:

```bash
python3 scripts/validate-site.py
node scripts/test-guide.cjs
```

El favicon usa la «M» geométrica sobre el azul oscuro de la web. Se incluye en
SVG, ICO (16, 32, 48 y 64 píxeles) y PNG para accesos directos de Apple.
Se regenera con `python3 scripts/build-icons.py`.
