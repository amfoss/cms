from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Photo)
class PhotoAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = [
                ('uploader', 'date'),
                'image',
                'caption'
             ]
    list_display = ('caption', 'uploader', 'date')
    list_filter = ['date']
    search_fields = ['uploader']
    select2 = select2_modelform(Photo, attrs={'width': '250px'})
    form = select2


@admin.register(Album)
class AlbumAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = [
                'title',
                ('uploader', 'date'),
                'description',
                'photos',
            ]
    list_display = ('title', 'uploader', 'date')
    list_filter = ('date',)
    search_fields = ['uploader']
    select2 = select2_modelform(Album, attrs={'width': '250px'})
    form = select2
