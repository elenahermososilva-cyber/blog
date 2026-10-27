# Visión: blog de robótica

## Propósito

Crear un espacio en español donde las personas interesadas en la robótica puedan descubrir ideas, seguir aprendiendo y conocer a quien las comparte. El blog debe hacer que leer un artículo sea sencillo y agradable, tanto desde un móvil como desde un ordenador.

## Experiencia deseada

La portada orienta al visitante hacia los artículos recientes con sus imágenes de portada; cada artículo ofrece una lectura clara y completa, con imágenes insertadas junto al texto cuando ayudan a explicarlo, y la sección «Sobre mí» permite conocer al autor. La navegación es directa y accesible, y el contenido, no las funciones accesorias, ocupa el centro de la experiencia.

El sitio también debe ser fácil de mantener: el editor puede actualizar los artículos y la presentación del autor mediante el panel de administración de Django, sin modificar las plantillas. Los visitantes no necesitan una cuenta ni se les pide participar para leer.

Además, integraciones autorizadas pueden consultar en JSON los artículos publicados y enviar borradores mediante una API REST. La escritura queda restringida a administradores; la publicación sigue siendo una acción editorial en Django Admin.

## Principios

- **Lectura primero:** priorizar una estructura comprensible, texto legible y una presentación sin elementos innecesarios.
- **Imágenes con propósito:** complementar los artículos con imágenes adaptables, descripciones alternativas y pies de foto cuando aporten contexto.
- **Acceso sencillo:** ofrecer navegación clara, HTML semántico y una experiencia adaptable y utilizable con teclado.
- **Contenido mantenible:** permitir que el editor gestione publicaciones y presentación desde Django Admin, con borradores ocultos a los visitantes.
- **Alcance deliberado:** centrarse en publicar y leer artículos, sin añadir cuentas públicas, comentarios, suscripciones ni otras funciones sociales.

## Señales de éxito

- Una persona encuentra un artículo en la portada y puede leerlo completo.
- Las imágenes de portada y las imágenes insertadas se muestran correctamente, también en pantallas pequeñas.
- La sección «Sobre mí» es fácil de localizar desde las páginas del sitio.
- La experiencia conserva su legibilidad y navegación en pantallas pequeñas y grandes.
- El editor puede sustituir el contenido de ejemplo y mantener el sitio sin editar código de plantillas.
