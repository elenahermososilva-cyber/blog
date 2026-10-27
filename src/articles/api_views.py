from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from .api_serializers import ArticleSerializer
from .models import Article


class PublishedArticleListCreateView(ListCreateAPIView):
    serializer_class = ArticleSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = Article.objects.filter(status=Article.Status.PUBLISHED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]


class PublishedArticleDetailView(RetrieveAPIView):
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    queryset = Article.objects.filter(status=Article.Status.PUBLISHED)
