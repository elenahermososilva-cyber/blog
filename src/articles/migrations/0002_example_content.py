from django.db import migrations
from django.utils import timezone


def create_example_content(apps, schema_editor):
    Article = apps.get_model('articles', 'Article')
    SiteProfile = apps.get_model('articles', 'SiteProfile')
    database = schema_editor.connection.alias

    SiteProfile.objects.using(database).get_or_create(
        pk=1,
        defaults={
            'display_name': 'Equipo de Bitácora Robótica',
            'biography': (
                'Somos un equipo curioso por la robótica y la tecnología. '
                'En este espacio compartimos ideas y proyectos para aprender '
                'cómo las máquinas perciben, deciden y actúan.'
            ),
        },
    )
    Article.objects.using(database).get_or_create(
        slug='que-es-un-robot',
        defaults={
            'title': '¿Qué es un robot?',
            'excerpt': (
                'Una introducción a los sensores, el control y los actuadores '
                'que permiten a un robot interactuar con el mundo.'
            ),
            'content': (
                'Un robot es una máquina programable capaz de percibir su '
                'entorno y actuar sobre él. No tiene por qué parecerse a una '
                'persona: puede ser un brazo industrial, un vehículo autónomo '
                'o un pequeño rover educativo.\n\n'
                '## Tres piezas fundamentales\n\n'
                'Los sensores recogen información, como la distancia a un '
                'obstáculo. El controlador interpreta esos datos y decide '
                'qué hacer. Finalmente, los actuadores convierten la decisión '
                'en movimiento, luz o sonido.\n\n'
                '### Un ciclo de percepción y acción\n\n'
                'El robot repite este ciclo: medir, decidir y actuar. Al '
                'probarlo en un entorno sencillo, por ejemplo siguiendo una '
                'línea, se entiende cómo cada pieza contribuye al resultado.'
            ),
            'author': 'Equipo de Bitácora Robótica',
            'published_at': timezone.now(),
            'status': 'published',
        },
    )
    Article.objects.using(database).get_or_create(
        slug='primeros-pasos-sensores',
        defaults={
            'title': 'Primeros pasos con sensores',
            'excerpt': (
                'Cómo empezar a experimentar con sensores de distancia y '
                'convertir una lectura en una acción sencilla.'
            ),
            'content': (
                'Los sensores ayudan a un robot a obtener información del '
                'entorno. Para empezar, basta con medir una variable y '
                'observar cómo cambia la lectura al mover un objeto.\n\n'
                '## De la medida a la decisión\n\n'
                'Un sensor de distancia puede indicar si hay un obstáculo '
                'cerca. El programa compara la medida con un umbral y, si es '
                'necesario, ordena detener un motor o encender una señal.\n\n'
                '### Experimenta con seguridad\n\n'
                'Prueba primero con velocidades bajas y una zona despejada. '
                'Anota las lecturas en distintas condiciones: observar sus '
                'límites es parte importante del aprendizaje.'
            ),
            'author': 'Equipo de Bitácora Robótica',
            'published_at': timezone.now(),
            'status': 'published',
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_example_content, migrations.RunPython.noop),
    ]
