# Criterios de aceptación: blog de robótica

Los criterios siguientes definen las condiciones verificables para dar por aceptada la primera versión. «Visitante» se refiere a una persona sin sesión iniciada; «editor autorizado», a una persona autenticada con permisos para gestionar el contenido.

## CA-01: Portada y artículos recientes

- Al solicitar `/`, se muestra la portada con el nombre del blog.
- La portada muestra únicamente artículos publicados, ordenados del más reciente al más antiguo.
- Cada artículo de la lista presenta título, fecha y extracto, y su enlace abre la página correspondiente.
- Si un artículo tiene imagen de portada, esta se muestra en su tarjeta sin impedir la navegación y se adapta al ancho disponible.
- Si no hay artículos publicados, la portada muestra un mensaje informativo y no deja la lista vacía sin explicación.

## CA-02: Lectura de artículos

- Al abrir la ruta de un artículo publicado, se muestran su título, fecha de publicación, autoría y contenido.
- El contenido conserva la separación en párrafos y subtítulos.
- La portada del artículo y las imágenes insertadas en el contenido se muestran con sus textos alternativos; los pies de foto configurados también aparecen.
- Cada imagen insertada aparece en la posición indicada por su marcador en el texto.
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
- Django Admin permite cargar o sustituir la imagen de portada y administrar las imágenes insertadas de cada artículo.

## CA-06: Adaptabilidad, accesibilidad y presentación

- La portada, el detalle de artículo y «Sobre mí» se pueden consultar en una pantalla móvil de 360 px de ancho y en una pantalla de escritorio de 1280 px, sin pérdida de contenido ni desplazamiento horizontal de la página.
- Las páginas usan estructura HTML semántica, una jerarquía coherente de encabezados y enlaces cuyo propósito se entiende por su texto.
- Los enlaces y controles principales son operables con teclado y muestran dónde está el foco.
- Las imágenes no provocan desplazamiento horizontal en móvil; las imágenes informativas cuentan con texto alternativo y las figuras admiten pies de foto.
- La presentación favorece la lectura prolongada mediante texto legible, espaciado adecuado y contraste suficiente.

## CA-07: Contenido inicial

- La base de datos recibe cuatro artículos de ejemplo relacionados con robótica, además de la presentación inicial del autor.
- Los dos artículos nuevos aparecen en la portada y sus páginas se pueden abrir como las demás publicaciones.

## CA-08: API REST de artículos

- `GET /api/articulos/` responde HTTP 200 con una lista JSON de artículos publicados y excluye todos los borradores.
- Cada objeto devuelto por la API incluye `id`, `titulo`, `cuerpo` y `estado`; para las publicaciones, `estado` es `publicado`.
- `GET /api/articulos/{id}/` devuelve esos mismos campos para un artículo publicado. Un borrador y un identificador inexistente responden HTTP 404.
- `POST /api/articulos/` acepta JSON con `titulo` y `cuerpo`, y solo permite la operación a un usuario de Django con `is_staff=True` que se autentique con `Authorization: Token <token>`.
- Si no se aporta un token válido, el POST responde HTTP 401; si el token pertenece a un usuario autenticado que no es personal, responde HTTP 403.
- Un POST válido devuelve HTTP 201 con `id`, `titulo`, `cuerpo` y `estado: "borrador"`. El servidor genera los campos restantes y no permite publicar el artículo mediante la API.
- Los campos `titulo` y `cuerpo` ausentes o vacíos se rechazan con HTTP 400 y errores JSON de validación.
- La API reutiliza `Article` y `published`; la web, Django Admin y los artículos existentes conservan su comportamiento.
