from django.db import models
from django.core.urlresolvers import reverse
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

    def __str__(self):
        return self.name


class GrId(models.Model):
    gr_id = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=400)
    ru_desc = models.TextField(null=True)
    en_desc = models.TextField(null=True)
    num_series = models.PositiveIntegerField(blank=True, null=True)
    gr_id = models.PositiveIntegerField(editable=False, blank=True, null=True)
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
    title = models.CharField(max_length=100, blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', max_length=200)
    book = models.ForeignKey(Book, blank=True, null=True)

    def __str__(self):
        return self.title


class Photos(models.Model):
    photo = models.ImageField(upload_to='authors_photo/', max_length=200, null=True)
    author = models.ForeignKey(Author, blank=True, null=True)


class Rating(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(MyUser)
    rating = models.IntegerField()

    def __str__(self):
        return self.rating