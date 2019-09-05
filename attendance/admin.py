from django.contrib import admin
from easy_select2 import select2_modelform
from datetime import datetime
from django.utils import timezone
from .models import *
from .generatorScript import generatorScript

@admin.register(Module)
class AttendanceModuleAdmin(admin.ModelAdmin):
    fields = (
        'name',
        ('seed', 'SSID'),
        ('seedRefreshInterval', 'lastRefreshTime')
    )
    list_display = ('name', 'SSID', 'lastRefreshTime', 'seedRefreshInterval')
    readonly_fields = ['SSID', 'lastRefreshTime']
    select2 = select2_modelform(Module, attrs={'width': '250px'})
    form = select2

    def save_model(self, request, obj, form, change):
        if 'seed' in form.changed_data:
            newSeed = generatorScript(obj.seed)
            obj.SSID = 'amFOSS_' + str(newSeed)
            obj.seed = newSeed
            obj.lastRefreshTime = timezone.now()
        super(AttendanceModuleAdmin, self).save_model(request, obj, form, change)

@admin.register(Log)
class AttendanceLogAdmin(admin.ModelAdmin):
    fields = (
        ('member', 'date', 'duration'),
        'modules',
        'sessions'
    )
    list_display = ('member', 'date', 'duration')
    select2 = select2_modelform(Log, attrs={'width': '250px'})
    form = select2


