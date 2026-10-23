from django.shortcuts import render

from .models import Article, SiteProfile


def home(request):
    articles = Article.objects.filter(status=Article.Status.PUBLISHED)
    return render(request, 'articles/home.html', {'articles': articles})


def article_detail(request, slug):
    article = Article.objects.filter(
        slug=slug,
        status=Article.Status.PUBLISHED,
    ).first()
    if article is None:
        return render(request, '404.html', status=404)
    return render(request, 'articles/article_detail.html', {'article': article})


def about(request):
    profile = SiteProfile.objects.first()
    return render(request, 'articles/about.html', {'profile': profile})


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
