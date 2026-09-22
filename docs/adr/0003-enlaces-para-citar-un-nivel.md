# 3. Un nivel se cita con `?nivel=N` en la portada, que lo muestra en un modal

Fecha: 2026-09-22 · Estado: aceptado

## Contexto

Quien cita el MIAE en otra web quiere enlazar un nivel concreto y que, al
pulsar, aparezca su descripción sin tener que buscarla en el documento
completo. Ya existían los anclajes `#nivel-N` del texto completo, pero llevan a
un punto dentro de un documento largo y no destacan el nivel.

## Decisión

La dirección para citar un nivel es `https://jjdeharo.github.io/miae/<idioma>/?nivel=N`
(N de 0 a 5). La portada de ese idioma se abre y muestra un modal (`<dialog>`)
con el número, el nombre y el resumen del nivel, con dos acciones: cerrar o ir
a la descripción completa (`v2.1/<idioma>/#nivel-N`). Al cerrar, el parámetro
se retira de la URL. Con un nivel inválido no ocurre nada. La raíz
`https://jjdeharo.github.io/miae/?nivel=N` también vale: elige el idioma del
navegador y conserva el parámetro (véase el ADR 2).

El resumen del modal sale del apartado «Resumen de niveles» del Markdown de
cada idioma, que el script parsea al construir; no hay un segundo texto que
mantener. Los seis resúmenes van incrustados en la portada, así el modal no
necesita cargar nada.

Para obtener la dirección hay un botón con el icono de compartir (Lucide
`share-2`) en cada celda del espectro de la portada y en el título de cada
nivel del documento completo. Al pulsarlo se copia la dirección al
portapapeles y se avisa con «Enlace copiado»; si el portapapeles no está
disponible, el aviso muestra la propia dirección. En el documento el control es
un enlace a esa dirección, así funciona también sin JavaScript.

## Alternativas descartadas

- Usar el fragmento (`#nivel-N`) también para el modal: ya está reservado para
  el anclaje del documento y no distingue «ir al texto» de «mostrar el resumen».
- Abrir el modal sobre el documento completo en lugar de la portada: la portada
  carga más ligera y sitúa el nivel entre los seis.
- Ofrecer el panel de compartir del sistema (Web Share): solo existe en móvil y
  en algunos navegadores; copiar el enlace funciona igual en todos.

## Consecuencias

El parámetro `nivel` queda reservado en la portada. Si cambia el número o el
formato de los resúmenes en el Markdown, el script avisa al construir. Los
botones de compartir no salen en la impresión ni en los PDF.
