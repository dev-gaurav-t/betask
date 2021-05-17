from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from articles.models import Article, Tag
from articles.serializers import ArticleSerializer, TagSerializer


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ['title', 'created_at']
    filterset_fields = ['title', 'content']

    def get_queryset(self):
        queryset = Article.objects.all()
        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                tags = list(Tag.objects.filter(parent=tag.id).values_list('id'))
                tags.append(tag.id)
                queryset = queryset.filter(tags__in=tags)
            except Tag.DoesNotExist:
                queryset = Article.objects.none()
        return queryset


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleAddTagAPIView(APIView):

    def put(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        tag = get_object_or_404(Tag, pk=request.data.get('tag'))

        article.tags.add(tag)
        article.save()
        article_ser = ArticleSerializer(article)
        return Response(data=article_ser.data)

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        tag = get_object_or_404(Tag, pk=request.data.get('tag'))

        article.tags.remove(tag)
        article.save()
        article_ser = ArticleSerializer(article)
        return Response(data=article_ser.data)


class TagListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
