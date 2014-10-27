from django.conf.urls import patterns, url, include
from users import views

urlpatterns = patterns('',
    url(r'^$', views.users_index, name='users_index'),
    url(r'^(?P<user_nickname>\w+)/$', views.user_detail, name='user_detail'),
)