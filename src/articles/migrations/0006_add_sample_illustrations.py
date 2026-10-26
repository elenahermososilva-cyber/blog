from django.db import migrations


SAMPLE_ILLUSTRATIONS = {
    'que-es-un-robot': {
        'illustration': 'robot',
        'marker': 'robot-explorador',
        'alt_text': 'Ilustración de un robot explorador con sensores y ruedas.',
        'caption': 'Un robot combina sensores, control y movimiento.',
    },
    'primeros-pasos-sensores': {
        'illustration': 'sensor',
        'marker': 'sensor-de-distancia',
        'alt_text': 'Ilustración de un sensor de distancia emitiendo ondas.',
        'caption': 'El sensor detecta objetos mediante ondas de distancia.',
    },
    'del-sensor-al-movimiento': {
        'illustration': 'controller',
        'marker': 'placa-controladora',
        'alt_text': 'Ilustración de una placa controladora con circuitos.',
        'caption': 'El controlador procesa las lecturas y dirige los motores.',
    },
    'como-se-orienta-un-robot-movil': {
        'illustration': 'navigation',
        'marker': 'ruta-del-robot',
        'alt_text': 'Ilustración de un robot móvil siguiendo una ruta.',
        'caption': 'El robot estima su posición para recorrer la ruta.',
    },
}


def add_sample_illustrations(apps, schema_editor):
    Article = apps.get_model('articles', 'Article')
    ArticleImage = apps.get_model('articles', 'ArticleImage')
    database = schema_editor.connection.alias

    for slug, sample in SAMPLE_ILLUSTRATIONS.items():
        article = Article.objects.using(database).filter(slug=slug).first()
        if article is None:
            continue

        if not article.cover_image and not article.cover_illustration:
            article.cover_illustration = sample['illustration']
            article.save(using=database, update_fields=['cover_illustration'])

        marker_token = f"[[imagen:{sample['marker']}]]"
        if marker_token not in article.content:
            first_paragraph, separator, remaining_content = article.content.partition('\n\n')
            article.content = (
                f'{first_paragraph}\n\n{marker_token}'
                f'{separator}{remaining_content}'
            )
            article.save(using=database, update_fields=['content'])

        ArticleImage.objects.using(database).get_or_create(
            article_id=article.pk,
            marker=sample['marker'],
            defaults={
                'illustration': sample['illustration'],
                'alt_text': sample['alt_text'],
                'caption': sample['caption'],
                'position': 1,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('articles', '0005_article_cover_illustration_articleimage_illustration_and_more'),
    ]

    operations = [
        migrations.RunPython(
            add_sample_illustrations,
            migrations.RunPython.noop,
        ),
    ]
