from django.contrib import admin
from books.models import Book, Author, Series, Covers

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Series)
admin.site.register(Covers)