from django.contrib import admin
from easy_select2 import select2_modelform
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from .models import *
from .inlines import *


class FormResource(resources.ModelResource):

    class Meta:
        model = Form


@admin.register(Form)
class FormAdmin(ImportExportModelAdmin, ExportActionMixin,admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                        'name',
                        'admins',
                        'submissionDeadline',
                        ('allowMultiple', 'admissionLimit', 'isActive'),
                      ]
        }),
        ('Form Fields', {
            'fields': [
                        'formFields'
                      ]
        }),

    ]
    list_display = ('name', 'isActive', 'allowMultiple', 'submissionDeadline', 'admissionLimit')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    inlines = (FormSlotInline, )
    form = select2
    resource_class = FormResource


class EntryResource(resources.ModelResource):
    firstPreference = Field()

    class Meta:
        model = Entry
        fields = ('id', 'form', 'name', 'email', 'phone', 'formData', 'slot', 'firstPreference', 'submissionTime')

    def dehydrate_firstPreference(self, entry):
        return entry.slot.slot.name

@admin.register(Entry)
class EntryAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'name',
                ('form', 'slot'),
                ('email', 'phone', 'submissionTime'),
            ]
        }),
        ('Form Fields', {
            'fields': [
                'formData'
            ]
        }),
    ]
    list_display = ('name', 'form', 'slot', 'phone', 'submissionTime')
    select2 = select2_modelform(Entry, attrs={'width': '250px'})
    form = select2
    resource_class = EntryResource


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    readonly_fields = (id, )
