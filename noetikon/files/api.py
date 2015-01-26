import os

from braces.views import LoginRequiredMixin
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_text
from django.views.generic import View

from noetikon.files.forms import UploadForm
from noetikon.files.models import Directory


class UploadFileView(LoginRequiredMixin, View):

    def post(self, request, directory_id):
        directory = self.get_object(request.user, directory_id)
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = request.FILES['file']
            path = smart_text(os.path.join(directory.path, new_file.name))
            if os.path.exists(path):
                return JsonResponse({'message': 'Image already exists on server'}, status=400)

            self.write_file(path, new_file)
            return JsonResponse({'message': 'Successfully uploaded image'}, status=200)

    def get_object(self, user, directory_id):
        return get_object_or_404(Directory.objects.permitted(user), pk=directory_id)

    def write_file(self, path, new_file):
        with open(path, 'wb+') as destination:
            for chunk in new_file.chunks():
                destination.write(chunk)
