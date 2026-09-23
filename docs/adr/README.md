# Decisiones de arquitectura (ADR)

Cada archivo recoge una decisión que condiciona el trabajo futuro: por qué se
tomó, qué se descartó y qué consecuencias tiene. Sirven para que nadie las
deshaga después de buena fe, ni siquiera nosotros dentro de un año.

| Nº | Decisión | Estado |
|---|---|---|
| [1](0001-web-estatica-generada-desde-markdown.md) | La web se genera con un script a partir del texto en Markdown, con una URL permanente por versión | aceptado |
| [2](0002-idioma-automatico-con-url-explicitas.md) | Las entradas neutras eligen el idioma del navegador; las URL con idioma se conservan | aceptado |
| [3](0003-enlaces-para-citar-un-nivel.md) | Un nivel se cita con `?nivel=N` en la portada, que lo muestra en un modal | aceptado |
| [4](0004-el-tema-claro-u-oscuro-sigue-al-dispositivo-con-un-conmutador.md) | El tema claro u oscuro sigue al dispositivo, con un conmutador | aceptado |

Para añadir una, se ejecuta `nuevo-adr "Título de la decisión"` desde la raíz
del repositorio (o se copia [la plantilla](0000-plantilla.md) con el número
siguiente) y se anota aquí. Una decisión que deje de valer no se borra: se
marca como «sustituida por» la nueva, para que quede el rastro.
