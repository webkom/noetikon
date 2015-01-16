from django.conf.urls import url

from .views import DirectoryListView, DirectoryDetailView

urlpatterns = [
    url(r'^$', DirectoryListView.as_view(), name='directory-list'),
    url(r'^(?P<slug>[a-zA-Z0-9\-/_ ]+)/$', DirectoryDetailView.as_view(), name='directory-detail')
]
