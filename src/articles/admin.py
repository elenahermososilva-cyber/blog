from django.contrib import admin

from .models import Article, ArticleImage, SiteProfile


class ArticleImageInline(admin.StackedInline):
    model = ArticleImage
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'status')
    list_filter = ('status', 'published_at')
    search_fields = ('title', 'excerpt', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    inlines = (ArticleImageInline,)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'slug',
                'excerpt',
                'cover_image',
                'cover_illustration',
                'cover_alt',
                'content',
            ),
            'description': (
                'Para colocar una imagen dentro del texto, añade su marcador '
                'en una línea independiente con el formato [[imagen:marcador]]. '
                'Configura ese mismo marcador en la imagen relacionada. Los '
                'artículos de ejemplo incluyen ilustraciones que puedes '
                'conservar o sustituir.'
            ),
        }),
        ('Publicación', {'fields': ('author', 'published_at', 'status')}),
    )


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name',)

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()
