from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform

from .generatorScript import generatorScript

@admin.register(Thread)
class AttendanceThreadAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Secrets', {
            'fields': (
                ('seed', 'SSID'),
            )
        }),
        ('Timings', {
            'fields': (
                ('seedRefreshInterval', 'lastRefreshTime'),
            )
        }),
    )
    list_display = ('name', 'SSID', 'lastRefreshTime', 'seedRefreshInterval')
    readonly_fields = ['SSID', 'lastRefreshTime']
    select2 = select2_modelform(Thread, attrs={'width': '250px'})
    form = select2

    def save_model(self, request, obj, form, change):
        if 'seed' in form.changed_data:
            newSeed = generatorScript(obj.seed)
            obj.SSID = 'amFOSS_' + str(newSeed)
            obj.seed = newSeed
        super(AttendanceThreadAdmin, self).save_model(request, obj, form, change)

@admin.register(Log)
class AttendanceLogAdmin(admin.ModelAdmin):
    fields = (
        ('member', 'date', 'duration'),
        'threads',
        'sessions'
    )
    list_display = ('member', 'date', 'duration')
    select2 = select2_modelform(Log, attrs={'width': '250px'})
    form = select2


