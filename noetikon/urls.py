from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^accounts/', include('nopassword.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('noetikon.files.urls')),
)
