import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator


class Illustration(models.TextChoices):
    ROBOT = 'robot', 'Robot explorador'
    SENSOR = 'sensor', 'Sensor de distancia'
    CONTROLLER = 'controller', 'Placa controladora'
    NAVIGATION = 'navigation', 'Ruta de navegación'


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        PUBLISHED = 'published', 'Publicado'

    title = models.CharField('título', max_length=200)
    slug = models.SlugField('URL', max_length=220, unique=True)
    excerpt = models.CharField('extracto', max_length=300, blank=True)
    content = models.TextField('contenido')
    cover_image = models.ImageField(
        'imagen de portada',
        upload_to='articles/covers/',
        blank=True,
    )
    cover_illustration = models.CharField(
        'ilustración de portada',
        max_length=20,
        choices=Illustration.choices,
        blank=True,
        help_text='Ilustración de ejemplo. Una imagen cargada tiene prioridad.',
    )
    cover_alt = models.CharField(
        'texto alternativo de portada',
        max_length=200,
        blank=True,
        help_text='Describe la imagen para quienes usan lectores de pantalla.',
    )
    author = models.CharField(
        'autoría',
        max_length=120,
        default='Equipo de Bitácora Robótica',
    )
    published_at = models.DateTimeField(
        'fecha de publicación',
        default=timezone.now,
    )
    status = models.CharField(
        'estado',
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ['-published_at', '-pk']
        verbose_name = 'artículo'
        verbose_name_plural = 'artículos'

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.cover_image and not self.cover_alt.strip():
            raise ValidationError({
                'cover_alt': 'Describe la imagen de portada en el texto alternativo.',
            })

    @property
    def summary(self):
        if self.excerpt:
            return self.excerpt
        normalized_content = self.content.replace('\r\n', '\n').replace('\r', '\n')
        plain_text = re.sub(r'^#{1,3}\s+', '', normalized_content, flags=re.MULTILINE)
        plain_text = re.sub(
            r'^\[\[imagen:[a-zA-Z0-9_-]+\]\]\s*$',
            '',
            plain_text,
            flags=re.MULTILINE,
        )
        return Truncator(plain_text).words(35)


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='inline_images',
        verbose_name='artículo',
    )
    marker = models.SlugField(
        'marcador en el texto',
        max_length=80,
        help_text='Identificador para insertar la imagen, por ejemplo: sensor.',
    )
    image = models.ImageField(
        'imagen',
        upload_to='articles/inline/',
        blank=True,
    )
    illustration = models.CharField(
        'ilustración de ejemplo',
        max_length=20,
        choices=Illustration.choices,
        blank=True,
    )
    alt_text = models.CharField(
        'texto alternativo',
        max_length=200,
        help_text='Describe la imagen para quienes usan lectores de pantalla.',
    )
    caption = models.CharField('pie de foto', max_length=200, blank=True)
    position = models.PositiveIntegerField('orden', default=0)

    class Meta:
        ordering = ['position', 'pk']
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'marker'],
                name='unique_article_image_marker',
            ),
        ]
        verbose_name = 'imagen dentro del artículo'
        verbose_name_plural = 'imágenes dentro del artículo'

    def __str__(self):
        return f'{self.article}: {self.marker}'

    def clean(self):
        super().clean()
        if bool(self.image) == bool(self.illustration):
            raise ValidationError(
                'Selecciona una imagen cargada o una ilustración de ejemplo, '
                'pero no ambas.'
            )


class SiteProfile(models.Model):
    display_name = models.CharField(
        'nombre del autor',
        max_length=120,
        default='Autor del blog',
    )
    biography = models.TextField(
        'presentación',
        help_text='Separa los párrafos con una línea en blanco.',
    )

    class Meta:
        verbose_name = 'presentación del autor'
        verbose_name_plural = 'presentación del autor'

    def __str__(self):
        return self.display_name
