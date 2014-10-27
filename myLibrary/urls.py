from django.conf.urls import patterns, include, url
from django.contrib import admin
from books import views
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^blog/', include('blog.urls')),
                       url(r'^books/', include('books.urls')),
                       url(r'^author/(?P<author_id>\d+)/$', views.author_detail, name='author_detail'),
                       url(r'^series/(?P<series_id>\d+)/$', views.series_detail, name='series_detail'),
                       url(r'^series/$', views.series_index, name='series_index'),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^users/', include('users.urls'))
                       )

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))