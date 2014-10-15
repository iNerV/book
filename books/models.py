from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='/', max_length=200, null=True)  # FIXME разобраться
    gender = models.CharField(max_length=6, null=True, blank=True)
    birth_date = models.CharField(max_length=200, null=True, blank=True)
    site = models.URLField(blank=True, null=True)


class Series(models.Model):
    gr_id = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True)


class GrId(models.Model):
    gr_id = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=400)
    author = models.ManyToManyField(Author)
    num_series = models.PositiveIntegerField()
    ru_desc = models.TextField(null=True)
    en_desc = models.TextField(null=True)
    other_desc = models.TextField(null=True)
    book_cover = models.ImageField(upload_to='/', max_length=200)  # FIXME возможно нужна другая таблица
    isbn10 = models.PositiveIntegerField(null=True, max_length=10)
    isbn13 = models.PositiveIntegerField(null=True, max_length=13)
    asin = models.CharField(null=True, max_length=10)
    series = models.ManyToManyField(Series, null=True)
    url = models.PositiveIntegerField()  # FIXME возможно нужна другая таблица