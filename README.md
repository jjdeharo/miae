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
