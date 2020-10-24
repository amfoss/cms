from django.contrib import admin
from activity.models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from easy_select2 import select2_modelform
import requests
from utilities.models import Token


@admin.register(News)
class NewsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('author', 'pinned'),
                ('title', 'slug', 'cover'),
                ('date', 'category'),
                'tags',
                ('description', 'rebuild')
            ]
        }),
    ]
    list_display = ('title', 'category', 'pinned')
    list_filter = ('category', 'pinned', 'tags')

    def save_model(self, request, obj, form, change):
        if obj.rebuild is True:
            TRIGGER_TOKEN = Token.objects.values().get(key='TRIGGER_TOKEN')['value']
            url = 'https://gitlab.com/api/v4/projects/16307254/trigger/pipeline'
            data = {'ref': 'master', 'token': TRIGGER_TOKEN}
            x = requests.post(url, data=data)
            obj.rebuild = False
        super(NewsAdmin, self).save_model(request, obj, form, change)


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
