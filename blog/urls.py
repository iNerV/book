#coding: utf-8
from django.conf.urls import patterns, url
from blog.views import PostsListView, PostDetailView
from blog import views

urlpatterns = patterns('',
                        url(r'^$', PostsListView.as_view(), name='list'),
                        url(r'^(?P<pk>\d+)/$', PostDetailView.as_view()),
                        url(r'^add_post/$', views.add_post, name='add_post'),
                        )