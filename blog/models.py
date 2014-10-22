from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)  # заголовок поста
    datetime = models.DateTimeField(u'Дата публикации')  # дата публикации
    content = models.TextField(max_length=10000, blank=True)  # текст поста
    content_short = models.TextField(max_length=1000)  # короткий текст поста

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%i/" % self.id