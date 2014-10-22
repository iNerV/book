from django.db import models
from django.core.urlresolvers import reverse


class Author(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=6, null=True, blank=True)
    birth_date = models.CharField(max_length=200, null=True, blank=True)
    site = models.URLField(blank=True, null=True)


class Series(models.Model):
    gr_id = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)


class GrId(models.Model):
    gr_id = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=400)
    ru_desc = models.TextField(null=True)
    en_desc = models.TextField(null=True)
    num_series = models.PositiveIntegerField(blank=True, null=True)
    gr_id = models.PositiveIntegerField()
    series = models.ManyToManyField(Series, blank=True, null=True)
    author = models.ManyToManyField(Author)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('books.views.details', args=[str(self.id)])


class Titles(models.Model):
    title = models.CharField(max_length=400)
    book = models.ForeignKey(Book, blank=True, null=True)


class ISBN10(models.Model):
    isbn10 = models.CharField(max_length=10)
    book = models.ForeignKey(Book, blank=True, null=True)


class ISBN13(models.Model):
    isbn13 = models.CharField(max_length=13)
    book = models.ForeignKey(Book, blank=True, null=True)


class ASIN(models.Model):
    asin = models.CharField(max_length=10)
    book = models.ForeignKey(Book, blank=True, null=True)


class Covers(models.Model):
    cover = models.ImageField(upload_to='/covers/', max_length=200)
    book = models.ForeignKey(Book, blank=True, null=True)


class Photos(models.Model):
    photo = models.ImageField(upload_to='/authors_photo/', max_length=200, null=True)
    author = models.ForeignKey(Author, blank=True, null=True)