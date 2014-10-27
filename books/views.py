from django.shortcuts import get_object_or_404, render
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from django.views import generic
from books.models import Book, Author, ISBN10, ISBN13, ASIN, Series, Titles, Covers, Photos


def books_index(request):
    books_list = Book.objects.prefetch_related('covers_set')
    return render(request, 'books/book_list.html', locals())


def series_index(request):
    series_list = Series.objects.all()
    context = {'series_list': series_list}
    return render(request, 'books/series_list.html', context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    author = Author.objects.get(book=book_id)
    series = Series.objects.get(book=book_id)
    isbn10 = ISBN10.objects.filter(book=book_id)
    isbn13 = ISBN13.objects.filter(book=book_id)
    asin = ASIN.objects.filter(book=book_id)
    title = Titles.objects.filter(book=book_id)
    cover = Covers.objects.filter(book=book_id)
    return render(request, 'books/book_detail.html', {
        'book': book,
        'author': author,
        'series': series,
        'isbn10': isbn10,
        'isbn13': isbn13,
        'asin': asin,
        'title': title,
        'cover': cover,
    })


def author_detail(request, author_id):
    author_info = get_object_or_404(Author, pk=author_id)
    books = Author.objects.get(id=author_id).book_set.all()
    photo = get_object_or_404(Photos, author_id=author_id)
    return render(request, 'books/author_info.html', {
        'author': author_info,
        'books': books,
        'photo': photo,
    })


def series_detail(request, series_id):
    series_info = get_object_or_404(Series, pk=series_id)
    books = Series.objects.get(id=series_id).book_set.all()
    return render(request, 'books/series_info.html', {
        'series': series_info,
        'books': books,
    })