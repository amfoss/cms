from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    fields = (
        'name',
        ( 'isActive', 'sendReport'),
        ('telegramGroupID', 'threadEmail'),
        'days',
        ('generationTime', 'dueTime', 'logTime'),
        'threadMessage'
    )
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    fields = ('date', ('thread', 'author'), 'subject', 'status')
    readonly_fields = ('date',)
    list_display = ('author', 'thread', 'date')
    list_filter = ('thread', 'author')
    search_fields = ['author__user', 'thread__name', 'subject', 'date']
    select2 = select2_modelform(Status, attrs={'width': '250px'})
    form = select2

@admin.register(StatusRegister)
class StatusRegisterAmdin(admin.ModelAdmin):
    list_display = ('member', 'timestamp')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields = (('title', 'date'), 'groups', 'description')
    select2 = select2_modelform(Notification, attrs={'width': '250px'})
    form = select2


