from django.contrib import admin

from .models import Directory, File


class DirectoryInline(admin.TabularInline):
    model = Directory
    extra = 0
    readonly_fields = ('path', 'size', 'exists', 'users_with_access', 'groups_with_access')


class FileInline(admin.TabularInline):
    model = File
    extra = 0
    readonly_fields = ('path', 'size', 'exists')


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'size', 'exists')
    inlines = [DirectoryInline, FileInline]
