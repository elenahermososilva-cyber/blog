from django.urls import path

from .api_views import (
    PublishedArticleDetailView,
    PublishedArticleListCreateView,
)

urlpatterns = [
    path(
        'articulos/',
        PublishedArticleListCreateView.as_view(),
        name='api_article_list_create',
    ),
    path(
        'articulos/<int:pk>/',
        PublishedArticleDetailView.as_view(),
        name='api_article_detail',
    ),
]
