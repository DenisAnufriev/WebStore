from django.db import models

from catalog.models import NULLABLE


class Article(models.Model):
    """
    Модель блога, представляющая статью.

    Эта модель содержит информацию о статье, включая заголовок, содержимое,
    фотографию, дату создания и статус публикации.
    """

    title = models.CharField(max_length=150, verbose_name="заголовок")
    slug = models.CharField(max_length=150, **NULLABLE)
    content = models.TextField(verbose_name="cодержимое статьи")
    photo = models.ImageField(upload_to="blog/photo", verbose_name="превью", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")
    views_count = models.IntegerField(default=0, verbose_name="просмотры")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
        ordering = ("-created_at",)
