from django.db import migrations
from django.utils import timezone


def create_more_examples(apps, schema_editor):
    Article = apps.get_model('articles', 'Article')
    database = schema_editor.connection.alias

    Article.objects.using(database).get_or_create(
        slug='del-sensor-al-movimiento',
        defaults={
            'title': 'Del sensor al movimiento',
            'excerpt': (
                'Descubre cómo un microcontrolador convierte las lecturas '
                'de los sensores en decisiones para un robot.'
            ),
            'content': (
                'Un sensor por sí solo solo produce datos. Para que un robot '
                'responda, un controlador debe leerlos, interpretarlos y '
                'decidir qué acción ejecutar.\n\n'
                '## El papel del microcontrolador\n\n'
                'El microcontrolador ejecuta instrucciones que conectan la '
                'entrada de los sensores con la salida de los motores. Una '
                'regla sencilla puede ordenar avanzar mientras no haya un '
                'obstáculo cerca y detenerse cuando la distancia sea menor '
                'que un umbral.\n\n'
                '### Probar y ajustar\n\n'
                'Las mediciones reales pueden variar. Prueba el programa con '
                'distancias distintas, observa cuándo cambia de decisión y '
                'ajusta el umbral para que el movimiento sea predecible.'
            ),
            'author': 'Equipo de Bitácora Robótica',
            'published_at': timezone.now(),
            'status': 'published',
        },
    )
    Article.objects.using(database).get_or_create(
        slug='como-se-orienta-un-robot-movil',
        defaults={
            'title': '¿Cómo se orienta un robot móvil?',
            'excerpt': (
                'Una introducción a la navegación: medir el entorno, '
                'estimar la posición y elegir una ruta.'
            ),
            'content': (
                'Para desplazarse, un robot móvil necesita estimar dónde '
                'está y qué hay a su alrededor. Puede combinar sensores de '
                'distancia, encoders en las ruedas y una representación '
                'sencilla del espacio.\n\n'
                '## Una ruta paso a paso\n\n'
                'Primero detecta obstáculos y referencias. Después estima '
                'su posición y compara el destino con el camino disponible. '
                'Con esa información puede elegir una dirección segura y '
                'corregir el rumbo mientras avanza.\n\n'
                '### La importancia de experimentar\n\n'
                'Las ruedas pueden resbalar y las lecturas no son perfectas. '
                'Un recorrido corto en un espacio despejado permite observar '
                'esas diferencias y mejorar poco a poco la navegación.'
            ),
            'author': 'Equipo de Bitácora Robótica',
            'published_at': timezone.now(),
            'status': 'published',
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0003_article_cover_alt_article_cover_image_articleimage'),
    ]

    operations = [
        migrations.RunPython(create_more_examples, migrations.RunPython.noop),
    ]
