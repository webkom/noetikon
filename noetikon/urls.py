from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^files/', include('noetikon.files.urls')),
    url(r'^api/', include('noetikon.api.urls', namespace='api', app_name='api')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('directory-list')))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if 'nopassword' in settings.INSTALLED_APPS:  # pragma: no cover
    urlpatterns.append(url(r'^accounts/', include('nopassword.urls')))
else:
    urlpatterns.append(url(r'^accounts/', include('django.contrib.auth.urls')))
