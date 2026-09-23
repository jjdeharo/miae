# 4. El tema claro u oscuro sigue al dispositivo, con un conmutador

Fecha: 2026-09-23 · Estado: aceptado

## Contexto

La web solo tenía tema claro. Las demás webs del autor (Sirena, la guía de vibe
coding, el decálogo) siguen el tema del dispositivo y llevan el mismo conmutador,
y se pidió lo mismo aquí por coherencia. No es un requisito de accesibilidad: las
WCAG piden contraste suficiente en el tema que se muestre, y el tema claro ya lo
cumplía.

## Decisión

- El tema sigue a `prefers-color-scheme` mientras no se elija otro con el botón
  luna/sol de la cabecera (portada, ficha y documento). La elección se guarda en
  `localStorage` como `miae-theme`; si coincide con la del dispositivo, se borra y
  la página vuelve a seguirlo. Un script en `<head>` aplica el tema antes de pintar.
- Los colores están en variables de `assets/site.css`. `--ink` es solo color de
  texto; los fondos oscuros de las bandas usan `--band`, y las tarjetas y campos,
  `--surface`, porque cambian de forma distinta en el tema oscuro.
- Los colores de los niveles (`--l0` a `--l5`) no cambian: siempre llevan texto
  blanco encima.
- El tema oscuro solo se aplica en pantalla. La impresión y los PDF salen siempre
  en claro, y la guía rápida, que es una hoja para imprimir, no tiene conmutador.

## Alternativas descartadas

- **Solo seguir al dispositivo, sin botón**: no permitiría a quien lee elegir,
  y no coincidiría con las demás webs del autor.
- **Oscurecer también la guía rápida**: es una hoja A4 pensada para el papel.

## Consecuencias

Un color nuevo en la hoja de estilos debe definirse con variables y tener su
valor oscuro. Las pruebas de accesibilidad deben pasarse en los dos temas.
