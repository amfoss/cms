from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('author', 'pinned'),
                ('title', 'slug', 'cover'),
                ('date', 'category'),
                'tags',
                'description'
            ]
        }),
    ]
    list_display = ('title', 'category', 'pinned')
    list_filter = ('category', 'pinned', 'tags')


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('name', 'author'),
            ]
        }),
    ]


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('name', 'author'),
            ]
        }),
    ]
