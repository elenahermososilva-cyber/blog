# Blog de robótica

Proyecto de un blog en español dedicado a la robótica, diseñado para ofrecer una experiencia de lectura sencilla, clara y adaptable a móviles y ordenadores. La portada reúne los artículos publicados más recientes; cada publicación cuenta con una página propia y el sitio incluye una sección «Sobre mí» para presentar al autor.

## Funcionalidades previstas

- Listado cronológico de artículos publicados, con título, fecha, extracto y enlace al contenido completo.
- Páginas de artículo con autoría y contenido organizado en párrafos y subtítulos.
- Sección «Sobre mí» editable.
- Gestión de artículos y presentación del autor mediante Django Admin, con borradores ocultos para los visitantes.
- Navegación accesible y diseño adaptable, centrados en la legibilidad y el contenido.

El proyecto no contempla cuentas para lectores, comentarios, suscripciones ni funciones sociales.

## Tecnología prevista

- Django para el servidor, las vistas y el renderizado de páginas.
- Plantillas HTML semánticas y CSS adaptable.
- SQLite para el desarrollo inicial.
- JavaScript solo si una necesidad concreta lo justifica.

## Estructura del proyecto

- `src/manage.py`: comandos de administración de Django.
- `src/config/`: configuración y enrutamiento principal del proyecto.
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

## Documentación

- [Briefing](./briefing.md): objetivo y alcance inicial.
- [Requisitos del producto](./PRD.md): requisitos funcionales, técnicos y criterios de éxito.
- [Especificación](./spec/vision.md): visión, alcance y criterios de aceptación.