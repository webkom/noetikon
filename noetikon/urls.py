from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('noetikon.files.urls')),
]

if 'nopassword' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^accounts/', include('nopassword.urls')))
else:
    urlpatterns.append(url(r'^accounts/', include('django.contrib.auth.urls')))
