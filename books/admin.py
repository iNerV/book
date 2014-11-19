from django.contrib import admin
from books.models import Book, Author, Series, Covers, Titles, ISBN13, ISBN10, ASIN, RuDesc, EnDesc


class CoversInline(admin.TabularInline):
    model = Covers
    extra = 1


class TitlesInline(admin.TabularInline):
    model = Titles
    extra = 1


class ISBN10Inline(admin.TabularInline):
    model = ISBN10
    extra = 1


class ISBN13Inline(admin.TabularInline):
    model = ISBN13
    extra = 1


class ASINInline(admin.TabularInline):
    model = ASIN
    extra = 1


class RuDescInline(admin.TabularInline):
    model = RuDesc
    extra = 1


class EnDescInline(admin.TabularInline):
    model = EnDesc
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = [RuDescInline, EnDescInline, CoversInline, TitlesInline, ISBN10Inline, ISBN13Inline, ASINInline]


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Series)