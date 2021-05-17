from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=32, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.slug

class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
