# Blog de robótica

Proyecto de un blog en español dedicado a la robótica, diseñado para ofrecer una experiencia de lectura sencilla, clara y adaptable a móviles y ordenadores. La portada reúne los artículos publicados más recientes; cada publicación cuenta con una página propia y el sitio incluye una sección «Sobre mí» para presentar al autor.

## Funcionalidades previstas

- Listado cronológico de artículos publicados, con título, fecha, extracto y enlace al contenido completo.
- Páginas de artículo con autoría, contenido organizado en párrafos y subtítulos, imagen de portada e imágenes insertadas.
- Sección «Sobre mí» editable.
- Gestión de artículos, imágenes y presentación del autor mediante Django Admin, con borradores ocultos para los visitantes.
- Navegación accesible y diseño adaptable, centrados en la legibilidad y el contenido.

El proyecto no contempla cuentas para lectores, comentarios, suscripciones ni funciones sociales.

## Tecnología prevista

- Django para el servidor, las vistas y el renderizado de páginas; Pillow para validar las imágenes.
- Plantillas HTML semánticas y CSS adaptable.
- SQLite para el desarrollo inicial.
- JavaScript solo si una necesidad concreta lo justifica.

## Estructura del proyecto

- `src/manage.py`: comandos de administración de Django.
- `src/config/`: configuración y enrutamiento principal del proyecto.
- `src/articles/`: aplicación del blog, modelos, vistas, plantillas, estilos y pruebas.
- `src/articles/api_urls.py`: rutas JSON de la API REST.
- `src/requirements.txt`: dependencias de Django.

## Preparación del entorno

Con Python instalado, crea y activa el entorno virtual desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell indica que la ejecución de scripts está deshabilitada, puedes permitirla solo en la terminal actual y volver a activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Este ajuste desaparece al cerrar esa terminal. Como alternativa, en una terminal del Símbolo del sistema (cmd) ejecuta:

```cmd
.venv\Scripts\activate.bat
```

También puedes usar directamente el Python del entorno sin activarlo: `.\.venv\Scripts\python.exe`.

Instala las dependencias del proyecto:

```powershell
python -m pip install -r src\requirements.txt
```

## Ejecutar en desarrollo

Desde la carpeta raíz del proyecto, inicia el servidor:

```powershell
python src\manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador. Para preparar la base de datos local, ejecuta antes:

```powershell
python src\manage.py migrate
```

Las migraciones cargan cuatro artículos, cada uno con una ilustración de portada y otra dentro del texto, además de una presentación de ejemplo. Puedes cambiar las ilustraciones por imágenes propias desde Django Admin en `http://127.0.0.1:8000/admin/`. Para acceder por primera vez al panel, crea un usuario administrador:

```powershell
python src\manage.py createsuperuser
```

En Django Admin puedes cargar una imagen de portada por artículo y añadir varias imágenes en línea desde «Imágenes dentro del artículo». Cada imagen en línea tiene un marcador único (por ejemplo, `sensor`) que puedes colocar en el texto con `[[imagen:sensor]]`, en una línea independiente. Añade texto alternativo para las imágenes en línea y para las portadas informativas. Los archivos subidos se guardan en `src\media` y se sirven desde `/media/` durante el desarrollo; en producción deben servirse desde un almacenamiento o servidor de medios configurado para el despliegue.

El contenido de los artículos también admite párrafos separados por líneas en blanco y subtítulos con `## ` o `### ` al inicio de una línea.

## API REST

La API permite consultar públicamente los artículos publicados y crear borradores solo con un token de un usuario de Django con acceso de personal (`is_staff`). No permite publicar artículos: los borradores se revisan y publican desde Django Admin.

- `GET /api/articulos/`: lista de artículos publicados.
- `GET /api/articulos/<id>/`: detalle de un artículo publicado; devuelve 404 para borradores o identificadores inexistentes.
- `POST /api/articulos/`: crea un borrador. Recibe JSON con `titulo` y `cuerpo`; responde con `id`, `titulo`, `cuerpo` y `estado`.

Para generar un token para un administrador existente, desde la carpeta raíz ejecuta:

```cmd
python src\manage.py drf_create_token TU_USUARIO
```

El comando muestra el token. Guárdalo de forma privada y no lo compartas ni lo publiques. Ejemplos para cmd (sustituye `TU_TOKEN` por el valor obtenido):

```cmd
curl.exe http://127.0.0.1:8000/api/articulos/
curl.exe http://127.0.0.1:8000/api/articulos/1/
curl.exe -X POST http://127.0.0.1:8000/api/articulos/ -H "Authorization: Token TU_TOKEN" -H "Content-Type: application/json" -d "{\"titulo\":\"Prueba API\",\"cuerpo\":\"Texto del borrador.\"}"
```

La respuesta del POST válido tiene HTTP 201 e incluye `"estado": "borrador"`. Los datos incompletos responden HTTP 400; las escrituras sin token válido se rechazan. En un sitio publicado, utiliza HTTPS para proteger el token en tránsito.

### Hacer un POST desde PowerShell usando el token de `.env`

Guarda el token en el archivo `.env`, en la carpeta raíz del proyecto, con este formato:

```env
BLOG_API_TOKEN=tu_token
```

Con el servidor ejecutándose, abre PowerShell en esa carpeta y ejecuta:

```powershell
$env:BLOG_API_TOKEN = (Get-Content .env | Where-Object { $_ -match '^BLOG_API_TOKEN=' } | Select-Object -First 1) -replace '^BLOG_API_TOKEN=', ''

$json = '{"titulo":"Prueba API VARIABLE","cuerpo":"Texto del borrador."}'
$bodyFile = Join-Path $env:TEMP 'blog-api-body.json'
[IO.File]::WriteAllText($bodyFile, $json, [Text.UTF8Encoding]::new($false))

curl.exe -X POST http://127.0.0.1:8000/api/articulos/ `
  -H "Authorization: Token $env:BLOG_API_TOKEN" `
  -H "Content-Type: application/json" `
  --data-binary "@$bodyFile"

Remove-Item $bodyFile
```

PowerShell no carga `.env` automáticamente, por eso el primer comando copia el token a la variable de entorno de la ventana actual. El archivo temporal evita problemas de comillas al pasar el JSON a `curl.exe`. El archivo `.env` está excluido de Git; no compartas ni publiques el token.

Ejecuta las pruebas con:

```powershell
python src\manage.py test articles
```

## Documentación

- [Briefing](./briefing.md): objetivo y alcance inicial.
- [Requisitos del producto](./PRD.md): requisitos funcionales, técnicos y criterios de éxito.
- [Especificación](./spec/vision.md): visión, alcance y criterios de aceptación.