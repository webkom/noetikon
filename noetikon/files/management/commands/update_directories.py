from django.core.management.base import BaseCommand

from noetikon.files.models import Directory


class Command(BaseCommand):

    def handle(self, *args, **options):
        for directory in Directory.objects.all():
            directory.update_content()
