from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


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
    search_fields =  ['name']
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('member', 'timestamp', 'thread')
    search_fields = ('member','thread')
    filter = ('thread',)