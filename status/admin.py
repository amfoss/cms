from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'enableGroupNotification')
        }),
        ('Timings', {
            'fields': (('days', 'generationTime', 'dueTime', 'logTime'),)
        }),
        ('Gmail Thread', {
            'fields': ('threadMessage',)
        }),
        ('Telegram Report', {
            'fields': ('footerMessage',)
        }),
    )
    list_display = ('name', 'enableGroupNotification', 'generationTime', 'dueTime', 'logTime')
    search_fields = ['name']
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2


class StatusUpdateResource(resources.ModelResource):
    class Meta:
        model = Log


@admin.register(Log)
class LogAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = [
        ('member', 'thread'),
        ('date', 'timestamp'),
    ]
    list_display = ('member', 'date', 'timestamp', 'thread')
    search_fields = ('member', 'thread')
    filter = ('thread',)
    resource_class = StatusUpdateResource
