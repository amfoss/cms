from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Log)
class AttendanceLogAdmin(admin.ModelAdmin):
    fields = (('member', 'date', 'duration'), 'sessions')
    list_display = ('member', 'date', 'duration')
    select2 = select2_modelform(Log, attrs={'width': '250px'})
    form = select2

