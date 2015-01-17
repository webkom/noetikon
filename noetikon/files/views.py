from braces.views._access import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from .models import Directory


class DirectoryListView(LoginRequiredMixin, ListView):
    model = Directory

    def get_queryset(self):
        return Directory.objects.filter(parent_folder=None)


class DirectoryDetailView(LoginRequiredMixin, DetailView):
    model = Directory
