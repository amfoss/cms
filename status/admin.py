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
    list_display = ('name', 'threadEmail', 'isActive', 'generationTime', 'dueTime', 'logTime')
    search_fields =  ['name']
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('member', 'timestamp')

