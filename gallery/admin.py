from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    fields = [
                ('uploader', 'date'),
                'image',
                'caption'
             ]
    list_display = ('image', 'uploader', 'date')
    list_filter = ['date']
    search_fields = ['uploader']
    select2 = select2_modelform(Photo, attrs={'width': '250px'})
    form = select2

    def has_module_permission(self, request):
        return False


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    fields = [
                'title',
                ('slug', 'uploader', 'date'),
                'description',
                 'cover',
                'photos',
                'featured'
            ]
    list_display = ('title', 'uploader', 'date')
    select2 = select2_modelform(Album, attrs={'width': '250px'})
    form = select2
