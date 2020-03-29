from django.contrib import admin
from easy_select2 import select2_modelform
from .models import *
from .generatorScript import generatorScript
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


class AttendanceModuleResource(resources.ModelResource):
    class Meta:
        model = Module


@admin.register(Module)
class AttendanceModuleAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = (
        'name',
        ('seed', 'SSID', 'isPaused'),
        ('seedRefreshInterval', 'lastRefreshTime')
    )
    list_display = ('name', 'SSID', 'lastRefreshTime', 'isPaused', 'seedRefreshInterval')
    readonly_fields = ['SSID', 'lastRefreshTime']
    select2 = select2_modelform(Module, attrs={'width': '250px'})
    form = select2

    def save_model(self, request, obj, form, change):
        if 'seed' in form.changed_data and obj.isPaused is False:
            newSeed = generatorScript(obj.seed)
            obj.SSID = 'amFOSS_' + str(newSeed)
            obj.seed = newSeed
            obj.lastRefreshTime = timezone.now().replace(second=0, microsecond=0)
        super(AttendanceModuleAdmin, self).save_model(request, obj, form, change)


class AttendanceLogResource(resources.ModelResource):
    class Meta:
        model = Log


@admin.register(Log)
class AttendanceLogAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = (
        ('member', 'date', 'duration'),
        ('modules', 'lastSeen'),
        'sessions'
    )
    list_display = ('member', 'date', 'lastSeen', 'duration')
    select2 = select2_modelform(Log, attrs={'width': '250px'})
    form = select2


