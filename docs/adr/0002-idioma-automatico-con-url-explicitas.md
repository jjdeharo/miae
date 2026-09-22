# 2. Las entradas neutras eligen el idioma del navegador; las URL con idioma se conservan

Fecha: 2026-09-07 · Estado: aceptado

## Contexto

La web está en castellano, catalán, euskera, gallego e inglés. Quien llega a la
raíz debería leerla en su idioma sin elegirlo, pero quien recibe un enlace a una
página concreta debe verla en el idioma en que se la enviaron.

## Decisión

Solo las entradas neutras (`/` y `/v2.1/`) redirigen, en el navegador, al
primer idioma compatible de las preferencias del sistema, con castellano como
alternativa; la redirección conserva la búsqueda y el fragmento de la URL. Las
direcciones con idioma (`/<idioma>/`, `/v2.1/<idioma>/`) nunca redirigen. El
selector permite guardar una elección manual en el navegador o volver a
«Automático». La lógica está en `assets/site.js` y se comprueba con
`node scripts/test-language.cjs`.

## Alternativas descartadas

- Redirigir también las páginas con idioma según la preferencia guardada: un
  enlace compartido dejaría de llevar a donde apunta.
- Negociación de idioma en el servidor: GitHub Pages no la ofrece.

## Consecuencias

Toda función nueva que dependa de la URL (por ejemplo, `?nivel=N`) debe
funcionar también tras la redirección, porque la búsqueda se conserva.
