from django.conf.urls import patterns, url, include
from books import views

urlpatterns = patterns('',
    url(r'^$', views.books_index, name='books_index'),
    url(r'^(?P<book_id>\d+)/$', views.book_detail, name='book_detail'),
)