from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from decimal import Decimal
from users.models import MyUser


class Author(models.Model):
    name = models.CharField(max_length=200, null=True)
    author_id = models.CharField(max_length=200)
    gender = models.CharField(max_length=6, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=200)
    gr_id = models.PositiveIntegerField()
    desc = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = u'Series'

    def __str__(self):
        return self.name


class GrId(models.Model):
    gr_id = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=400)
    ru_title = models.CharField(max_length=400)
    ru_desc = models.TextField(null=True)
    en_desc = models.TextField(null=True)
    num_series = models.PositiveIntegerField(blank=True, null=True)
    gr_id = models.PositiveIntegerField(editable=False, blank=True, null=True)
    series = models.ManyToManyField(Series)
    author = models.ManyToManyField(Author)
    fb_genres = models.ManyToManyField(FBGenres)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books.views.details', args=[str(self.id)])


class UserChanges(models.Model):
    STATE = ((0, _('Pending')),
             (1, _('Accepted')),
             (2, _('Rejected'))
             )

    user = models.ForeignKey(MyUser)  # FIXME возможно стоит сделать так же как с ReadList и передавать id вручную, надо проверять
    item_id = models.PositiveIntegerField()  # - id изменяемой сущности
    item_type = models.CharField()  # - имя изменяемого поля
    changes = models.TextField()  # - сериализованный массив с изменениями
    state = models.PositiveIntegerField(choices=STATE, default=0)  # - статус правки (pending, accepted, rejected, deleted
    approver_id = models.PositiveIntegerField()  # - ид принявшего/отказавшего/удалившего правку
    created_at = models.DateTimeField(auto_now_add=True)  # - дата создания
    updated_at = models.DateTimeField(auto_now=True, editable=False)  # - дата обновления


class Titles(models.Model):
    title = models.CharField(max_length=400)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.title


class ISBN10(models.Model):
    isbn10 = models.CharField(max_length=10)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.isbn10


class ISBN13(models.Model):
    isbn13 = models.CharField(max_length=13)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.isbn13


class ASIN(models.Model):
    asin = models.CharField(max_length=10)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.asin


class Covers(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', max_length=200)
    book = models.ForeignKey(Book)

    def __str__(self):
        return self.title


class Photos(models.Model):
    photo = models.ImageField(upload_to='authors_photo/', max_length=200, null=True)
    author = models.ForeignKey(Author, blank=True, null=True)


class FBGenres(models.Model):  # FictionBook Genres
    code = models.CharField()
    ru_name = models.CharField()
    en_name = models.CharField()


class OverallRating(models.Model):
    target_type = models.CharField()
    target_id = models.PositiveIntegerField()
    rating = models.DecimalField(null=True)  # Средний рейтинг
    scored_by = models.PositiveIntegerField(default=0)  # Количество проголосовавших TODO переименовать