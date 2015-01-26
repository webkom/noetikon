from django.conf.urls import url

from noetikon.files.api import UploadFileView

urlpatterns = [
    url(r'^files/(?P<directory_id>\d+)/upload', UploadFileView.as_view(), name='file-upload'),
]
