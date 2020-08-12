from django.contrib import admin
from activity.models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from easy_select2 import select2_modelform


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


@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('title', 'slug'),
                ('author', 'date', 'cover'),
                ('draft', 'featured', 'tags', 'category'),
                'description'
            ]
        }),
    ]
    list_display = ('title', 'slug', 'featured', 'date', 'category')
    list_filter = ('featured', 'category')
    select2 = select2_modelform(Blog, attrs={'width': '250px'})
    form = select2
