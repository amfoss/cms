from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import resources


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'isActive', 'enableGroupNotification', ('allowBotToKick', 'noOfDays'))
        }),
        ('Timings', {
            'fields': (('days', 'generationTime', 'dueTime', 'logTime'),)
        }),
        ('Mailing', {
            'fields': (('email',), 'threadMessage',)
        }),
        ('Reporting', {
            'fields': ('footerMessage',)
        }),
    )
    list_display = ('name', 'isActive', 'enableGroupNotification', 'allowBotToKick', 'generationTime', 'dueTime', 'logTime')
    search_fields = ['name']
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = [
        ('member', 'thread'),
        ('date', 'timestamp'),
        'message'
    ]
    list_display = ('member', 'date', 'timestamp', 'thread')
    search_fields = ('member__username', 'thread__name')
    filter = ('thread',)


@admin.register(StatusException)
class StatusExceptionAdmin(admin.ModelAdmin):
    fields = ['user', 'isPaused']

    list_display = ('user', 'isPaused')


class DailyLogResource(resources.ModelResource):
    class Meta:
        model = DailyLog


@admin.register(DailyLog)
class DailyLogAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = [
        ('date', 'thread'),
        'members',
        'late',
        'didNotSend'
    ]
    list_display = ('date', 'thread', 'totalCount', 'lateCount', 'didNotSendCount')
    select2 = select2_modelform(DailyLog, attrs={'width': '300px'})
    form = select2
    resource_class = DailyLogResource

    @staticmethod
    def totalCount(obj):
        return obj.members.count()

    @staticmethod
    def lateCount(obj):
        return obj.late.count()

    @staticmethod
    def didNotSendCount(obj):
        return obj.didNotSend.count()
