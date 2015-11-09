from django.conf.urls import url

from noetikon.files.views import FileDetailView

from .views import DirectoryDetailView, DirectoryListView, FileDownloadView

urlpatterns = [
    url(r'^$', DirectoryListView.as_view(), name='directory-list'),
    url(r'^download/(?P<slug>.+)/$', FileDownloadView.as_view(),
        name='file-download'),
    url(r'^view/(?P<slug>.+)/$', FileDetailView.as_view(), name='file-detail'),
    url(r'^(?P<slug>.+)/$', DirectoryDetailView.as_view(), name='directory-detail'),
]
