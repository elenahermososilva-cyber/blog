from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Article, ArticleImage, SiteProfile


def create_test_image(name='test.png'):
    image_file = BytesIO()
    Image.new('RGB', (40, 30), color='teal').save(image_file, format='PNG')
    return SimpleUploadedFile(
        name,
        image_file.getvalue(),
        content_type='image/png',
    )


class BlogPageTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Robots exploradores',
            slug='robots-exploradores',
            excerpt='Cómo se orienta un robot.',
            content='Un robot observa el entorno.\n\n## Sensores\n\nMiden distancias.',
            author='Ana Robótica',
            published_at=timezone.now(),
            status=Article.Status.PUBLISHED,
        )
        self.draft = Article.objects.create(
            title='Próximo experimento',
            slug='proximo-experimento',
            content='En preparación.',
            author='Ana Robótica',
            published_at=timezone.now(),
            status=Article.Status.DRAFT,
        )

    def test_home_lists_published_articles_and_hides_drafts(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Robots exploradores')
        self.assertContains(response, 'Cómo se orienta un robot.')
        self.assertNotContains(response, self.draft.title)

    def test_four_robotics_examples_are_available(self):
        example_slugs = (
            'que-es-un-robot',
            'primeros-pasos-sensores',
            'del-sensor-al-movimiento',
            'como-se-orienta-un-robot-movil',
        )

        self.assertEqual(
            Article.objects.filter(
                slug__in=example_slugs,
                status=Article.Status.PUBLISHED,
            ).count(),
            4,
        )

    def test_sample_articles_have_cover_and_inline_illustrations(self):
        articles = Article.objects.filter(
            slug__in=(
                'que-es-un-robot',
                'primeros-pasos-sensores',
                'del-sensor-al-movimiento',
                'como-se-orienta-un-robot-movil',
            )
        ).prefetch_related('inline_images')

        self.assertEqual(articles.count(), 4)
        for article in articles:
            with self.subTest(article=article.slug):
                self.assertTrue(article.cover_illustration)
                self.assertTrue(article.inline_images.exists())
                self.assertIn(
                    f'[[imagen:{article.inline_images.first().marker}]]',
                    article.content,
                )
                self.assertIsNotNone(
                    finders.find(
                        f'articles/images/{article.cover_illustration}.svg'
                    )
                )

                response = self.client.get(
                    reverse('article_detail', args=[article.slug])
                )
                self.assertContains(
                    response,
                    'class="article-figure article-cover-figure"',
                )
                self.assertContains(
                    response,
                    'class="article-figure"',
                )
                self.assertContains(
                    response,
                    f'/static/articles/images/{article.cover_illustration}.svg',
                )

    def test_home_shows_empty_state_without_published_articles(self):
        Article.objects.all().delete()

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Todavía no hay artículos publicados')

    def test_article_detail_renders_content_and_metadata(self):
        response = self.client.get(
            reverse('article_detail', args=[self.article.slug])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana Robótica')
        self.assertContains(response, '<h2>Sensores</h2>', html=True)
        self.assertContains(response, '<p>Miden distancias.</p>', html=True)
        self.assertContains(response, 'Volver a los artículos')

    def test_draft_and_missing_articles_return_404(self):
        draft_response = self.client.get(
            reverse('article_detail', args=[self.draft.slug])
        )
        missing_response = self.client.get(
            reverse('article_detail', args=['no-existe'])
        )

        self.assertEqual(draft_response.status_code, 404)
        self.assertEqual(missing_response.status_code, 404)
        self.assertContains(
            draft_response,
            '¡Un robot se ha llevado esta página!',
            status_code=404,
        )
        self.assertContains(
            missing_response,
            '¡Un robot se ha llevado esta página!',
            status_code=404,
        )

    def test_custom_404_page_is_used(self):
        with self.settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
            response = self.client.get('/ruta-inexistente/')

        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            '¡Un robot se ha llevado esta página!',
            status_code=404,
        )

    def test_about_page_shows_editable_profile(self):
        profile = SiteProfile.objects.first()
        profile.display_name = 'Ada Robótica'
        profile.biography = 'Construyo robots curiosos.\n\nMe gusta compartir.'
        profile.save()

        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sobre mí')
        self.assertContains(response, 'Ada Robótica')
        self.assertContains(response, '<p>Me gusta compartir.</p>', html=True)

    def test_admin_requires_authentication(self):
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)


class ArticleContentSafetyTests(TestCase):
    def test_content_formatter_escapes_html(self):
        article = Article.objects.create(
            title='Texto seguro',
            slug='texto-seguro',
            content='<script>alert("hola")</script>',
            author='Ana',
            status=Article.Status.PUBLISHED,
        )

        response = self.client.get(
            reverse('article_detail', args=[article.slug])
        )

        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_cover_image_is_shown_on_home_and_article(self):
        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                article = Article.objects.create(
                    title='Robots ilustrados',
                    slug='robots-ilustrados',
                    content='Un texto de ejemplo.',
                    cover_image=create_test_image('portada.png'),
                    cover_alt='Un robot de pruebas',
                    author='Ana',
                    status=Article.Status.PUBLISHED,
                )

                home_response = self.client.get(reverse('home'))
                detail_response = self.client.get(
                    reverse('article_detail', args=[article.slug])
                )

                self.assertContains(home_response, 'class="article-cover"')
                self.assertContains(
                    home_response,
                    'alt="" loading="lazy"',
                )
                self.assertContains(
                    detail_response,
                    'alt="Un robot de pruebas"',
                )
                self.assertContains(
                    detail_response,
                    '/media/articles/covers/portada',
                )
                self.assertTrue(
                    article.cover_image.storage.exists(article.cover_image.name)
                )

    def test_inline_image_renders_at_its_marker_with_alt_and_caption(self):
        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                article = Article.objects.create(
                    title='Dentro del robot',
                    slug='dentro-del-robot',
                    content=(
                        'Texto anterior.\n\n'
                        '[[imagen:placa-controladora]]\n\n'
                        'Texto posterior.'
                    ),
                    author='Ana',
                    status=Article.Status.PUBLISHED,
                )
                ArticleImage.objects.create(
                    article=article,
                    marker='placa-controladora',
                    image=create_test_image(),
                    alt_text='Placa con componentes electrónicos',
                    caption='Controlador principal del robot',
                )

                response = self.client.get(
                    reverse('article_detail', args=[article.slug])
                )
                content = response.content.decode()
                prose_start = content.index('<div class="prose">')

                self.assertEqual(response.status_code, 200)
                self.assertLess(
                    content.index('Texto anterior.', prose_start),
                    content.index('<figure class="article-figure">'),
                )
                self.assertLess(
                    content.index('<figure class="article-figure">'),
                    content.index('Texto posterior.', prose_start),
                )
                self.assertContains(
                    response,
                    'alt="Placa con componentes electrónicos"',
                )
                self.assertContains(response, 'Controlador principal del robot')


class ArticleApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Article.objects.all().delete()
        self.published_article = Article.objects.create(
            title='Artículo público',
            slug='articulo-publico',
            content='Contenido publicado.',
            status=Article.Status.PUBLISHED,
        )
        self.draft_article = Article.objects.create(
            title='Borrador privado',
            slug='borrador-privado',
            content='Contenido en preparación.',
            status=Article.Status.DRAFT,
        )

    def test_list_is_public_and_only_includes_published_articles(self):
        response = self.client.get(reverse('api_article_list_create'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0],
            {
                'id': self.published_article.pk,
                'titulo': 'Artículo público',
                'cuerpo': 'Contenido publicado.',
                'estado': 'publicado',
            },
        )

    def test_detail_is_public_and_hides_drafts_and_missing_articles(self):
        published_response = self.client.get(
            reverse('api_article_detail', args=[self.published_article.pk])
        )
        draft_response = self.client.get(
            reverse('api_article_detail', args=[self.draft_article.pk])
        )
        missing_response = self.client.get(
            reverse('api_article_detail', args=[999999])
        )

        self.assertEqual(published_response.status_code, 200)
        self.assertEqual(published_response.data['estado'], 'publicado')
        self.assertEqual(draft_response.status_code, 404)
        self.assertEqual(missing_response.status_code, 404)

    def test_post_requires_a_token_from_a_staff_user(self):
        url = reverse('api_article_list_create')
        payload = {'titulo': 'Nuevo artículo', 'cuerpo': 'Texto del artículo.'}

        anonymous_response = self.client.post(url, payload, format='json')
        self.assertEqual(anonymous_response.status_code, 401)

        user_model = get_user_model()
        regular_user = user_model.objects.create_user(
            username='lector',
            password='test-password',
        )
        regular_token = Token.objects.create(user=regular_user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Token {regular_token.key}'
        )
        regular_response = self.client.post(url, payload, format='json')
        self.assertEqual(regular_response.status_code, 403)

        admin_user = user_model.objects.create_user(
            username='editor',
            password='test-password',
            is_staff=True,
        )
        admin_token = Token.objects.create(user=admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        admin_response = self.client.post(url, payload, format='json')

        self.assertEqual(admin_response.status_code, 201)
        self.assertEqual(admin_response.data['estado'], 'borrador')

    def test_post_creates_a_draft_and_generates_a_unique_slug(self):
        Article.objects.create(
            title='Título existente',
            slug='prueba-api',
            content='Contenido publicado.',
            status=Article.Status.PUBLISHED,
        )
        user = get_user_model().objects.create_user(
            username='admin-api',
            password='test-password',
            is_staff=True,
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(
            reverse('api_article_list_create'),
            {
                'titulo': 'Prueba API',
                'cuerpo': 'Texto del borrador.',
                'estado': 'publicado',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            set(response.data),
            {'id', 'titulo', 'cuerpo', 'estado'},
        )
        self.assertEqual(response.data['estado'], 'borrador')
        article = Article.objects.get(pk=response.data['id'])
        self.assertEqual(article.slug, 'prueba-api-2')
        self.assertEqual(article.status, Article.Status.DRAFT)
        self.assertEqual(article.author, 'Equipo de Bitácora Robótica')

    def test_post_rejects_missing_or_blank_required_fields(self):
        user = get_user_model().objects.create_user(
            username='admin-validacion',
            password='test-password',
            is_staff=True,
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('api_article_list_create')

        missing_body = self.client.post(
            url,
            {'titulo': 'Artículo sin cuerpo'},
            format='json',
        )
        blank_title = self.client.post(
            url,
            {'titulo': '   ', 'cuerpo': 'Contenido.'},
            format='json',
        )

        self.assertEqual(missing_body.status_code, 400)
        self.assertIn('cuerpo', missing_body.data)
        self.assertEqual(blank_title.status_code, 400)
        self.assertIn('titulo', blank_title.data)
