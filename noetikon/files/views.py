from django.views.generic import ListView, DetailView

from .models import Directory


class DirectoryListView(ListView):
    model = Directory

    def get_queryset(self):
        return Directory.objects.filter(parent_folder=None)


class DirectoryDetailView(DetailView):
    model = Directory
