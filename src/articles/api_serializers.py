from django.utils.text import slugify
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source='title', max_length=200)
    cuerpo = serializers.CharField(source='content')
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'titulo', 'cuerpo', 'estado')
        read_only_fields = ('id', 'estado')

    def get_estado(self, article):
        if article.status == Article.Status.PUBLISHED:
            return 'publicado'
        return 'borrador'

    def create(self, validated_data):
        title = validated_data['title']
        return Article.objects.create(
            title=title,
            content=validated_data['content'],
            slug=self._unique_slug(title),
            status=Article.Status.DRAFT,
        )

    @staticmethod
    def _unique_slug(title):
        max_length = Article._meta.get_field('slug').max_length
        base_slug = slugify(title) or 'articulo'
        slug = base_slug[:max_length]
        suffix_number = 2
        while Article.objects.filter(slug=slug).exists():
            suffix = f'-{suffix_number}'
            slug = f'{base_slug[:max_length - len(suffix)]}{suffix}'
            suffix_number += 1
        return slug
