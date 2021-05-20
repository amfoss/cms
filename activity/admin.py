from django.contrib import admin
from activity.models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from easy_select2 import select2_modelform


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('author', 'pinned', 'featured'),
                ('title', 'slug', 'cover'),
                ('date', 'category'),
                'tags',
                'description'
            ]
        }),
    ]
    list_display = ('title', 'category', 'pinned', 'featured')
    list_filter = ('category', 'pinned', 'featured')
    select2 = select2_modelform(Blog, attrs={'width': '250px'})
    form = select2


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

@admin.register(Collection)
class CollectionAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('name', 'author','date'),
                ('cover')
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
                ('draft', 'featured','tags', 'category'),
                ('collection'),
                'description'
            ]
        }),
    ]
    list_display = ('title', 'slug', 'featured', 'date', 'category')
    list_filter = ('featured', 'category')
    select2 = select2_modelform(Blog, attrs={'width': '250px'})
    form = select2


@admin.register(Achievements)
class AchievementsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'title',
                ('user', 'year', 'category'),
                'description'
            ]
        }),
    ]

    list_display = ('title', 'user', 'year', 'category')
    list_filter = ('year', 'category')
