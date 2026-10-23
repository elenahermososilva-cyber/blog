# Criterios de aceptación: blog de robótica

Los criterios siguientes definen las condiciones verificables para dar por aceptada la primera versión. «Visitante» se refiere a una persona sin sesión iniciada; «editor autorizado», a una persona autenticada con permisos para gestionar el contenido.

## CA-01: Portada y artículos recientes

- Al solicitar `/`, se muestra la portada con el nombre del blog.
- La portada muestra únicamente artículos publicados, ordenados del más reciente al más antiguo.
- Cada artículo de la lista presenta título, fecha y extracto, y su enlace abre la página correspondiente.
- Si no hay artículos publicados, la portada muestra un mensaje informativo y no deja la lista vacía sin explicación.

## CA-02: Lectura de artículos

- Al abrir la ruta de un artículo publicado, se muestran su título, fecha de publicación, autoría y contenido.
- El contenido conserva la separación en párrafos y subtítulos.
- Una ruta de artículo inexistente devuelve HTTP 404 y muestra una página de error con un diseño humorístico.
- Un artículo no publicado no aparece en la portada ni puede consultarse mediante su URL pública.

## CA-03: Página «Sobre mí»

- Existe una página accesible en `/sobre-mi/` e identificable como «Sobre mí».
- La página muestra la presentación vigente del autor.
- Un editor autorizado puede sustituir esa presentación desde Django Admin y el cambio se refleja en la página pública.

## CA-04: Navegación

- La navegación principal ofrece enlaces descriptivos a la portada y a «Sobre mí» desde las páginas del sitio.
- Desde el detalle de un artículo se puede volver a la portada mediante un enlace claramente identificable.
- Los enlaces de navegación funcionan sin JavaScript y pueden recorrerse y activarse con teclado.

## CA-05: Gestión editorial y acceso

- Django Admin permite a un editor autorizado crear, editar y retirar artículos, y actualizar la presentación del autor.
- Los artículos admiten título, slug, contenido, autoría, fecha de publicación y estado de publicación.
- Una persona anónima no puede acceder a las funciones de edición; el acceso requiere autenticación y permisos autorizados.
- No existe un flujo público de registro ni una función para que visitantes creen o editen contenido.
- El contenido de ejemplo puede sustituirse o retirarse desde la gestión editorial.

## CA-06: Adaptabilidad, accesibilidad y presentación

- La portada, el detalle de artículo y «Sobre mí» se pueden consultar en una pantalla móvil de 360 px de ancho y en una pantalla de escritorio de 1280 px, sin pérdida de contenido ni desplazamiento horizontal de la página.
- Las páginas usan estructura HTML semántica, una jerarquía coherente de encabezados y enlaces cuyo propósito se entiende por su texto.
- Los enlaces y controles principales son operables con teclado y muestran dónde está el foco.
- La presentación favorece la lectura prolongada mediante texto legible, espaciado adecuado y contraste suficiente.
