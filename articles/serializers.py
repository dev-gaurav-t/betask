from rest_framework import serializers

from articles.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Article
        fields = "__all__"

    def create(self, data):
        tags = data.pop("tags")
        article = Article.objects.create(**data)
        for tag in tags:
            article.tags.add(Tag.objects.create(**tag).id)
        article.save()
        return article
