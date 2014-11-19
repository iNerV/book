from django.db import models
from django.utils import timezone
from users.models import MyUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(u'Дата публикации', default=timezone.now, blank=True)
    content = models.TextField(max_length=10000, blank=True)
    content_short = models.TextField(max_length=1000)
    author = models.ForeignKey(MyUser)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%i/" % self.id