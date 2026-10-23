# Alcance: blog de robótica

## Objetivo

Entregar una primera versión en español de un blog de robótica centrado en la lectura. Los visitantes podrán descubrir publicaciones recientes, leer artículos completos y conocer al autor.

## Incluido

- **Portada:** nombre del blog y artículos publicados recientes, ordenados del más nuevo al más antiguo. Cada artículo muestra imagen de portada si está disponible, título, fecha y extracto, y enlaza a su página. Si no hay publicaciones, se presenta un mensaje informativo.
- **Detalle del artículo:** página individual con título, fecha de publicación, autoría, imagen de portada opcional y contenido organizado en párrafos, subtítulos e imágenes insertadas. Las imágenes tienen texto alternativo y pueden incluir pie de foto. Las rutas inexistentes responden con una página 404 original (y a ser posible graciosa).
- **Sobre mí:** página con una presentación breve y editable del autor, accesible desde la navegación principal.
- **Navegación:** enlaces claros entre la portada y «Sobre mí», y una forma de volver a la portada desde cada artículo. La navegación básica funciona sin JavaScript.
- **Gestión editorial:** creación, edición y retirada de artículos, carga de imágenes de portada e imágenes insertadas, además de la actualización de la presentación, mediante el panel estándar de Django para editores autorizados. Los borradores no se muestran en las páginas públicas.
- **Contenido de inicio:** cuatro artículos de ejemplo sobre robótica y una presentación inicial, sustituibles o eliminables por el editor.
- **Experiencia de lectura:** páginas adaptables a móviles y escritorio, con HTML semántico, encabezados coherentes, enlaces descriptivos, uso por teclado y estilos que favorezcan la legibilidad.

## Fuera de alcance

- Registro, cuentas, perfiles o interacción para lectores.
- Comentarios, funciones sociales, suscripciones y boletines.
- Búsqueda de artículos.
- Flujos editoriales avanzados, como revisión, programación de publicaciones o varios roles editoriales.
- Funcionalidades que no sean necesarias para publicar, gestionar y leer el contenido descrito en este documento.

## Límites y supuestos

- El idioma inicial y el tema editorial son español y robótica, respectivamente.
- La primera versión contempla un editor y una única presentación principal del autor.
- La aplicación se implementará con Django, renderizado del lado del servidor y plantillas HTML; JavaScript solo se incorporará si surge una necesidad concreta.
- SQLite se utilizará para el desarrollo inicial. La base de datos de producción y el entorno de despliegue quedan pendientes de definir.
- Pillow se utilizará para validar las imágenes cargadas. Los medios se guardarán en `src/media` durante el desarrollo; el almacenamiento y la publicación de medios en producción se definirán con el despliegue.
- El diseño visual definitivo, el dominio y el contenido final no forman parte de las decisiones cerradas por este alcance.
