from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Directory, File


class DirectoryListView(LoginRequiredMixin, ListView):
    model = Directory

    def get_queryset(self):
        return Directory.objects.filter(parent_folder=None)


class DirectoryDetailView(LoginRequiredMixin, DetailView):
    model = Directory


class FileDownloadView(LoginRequiredMixin, SingleObjectMixin, View):

    model = File

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        response = HttpResponse()
        response['X-Accel-Redirect'] = instance.x_redirect_url
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.name
        return response
