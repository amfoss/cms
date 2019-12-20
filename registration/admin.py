from django.contrib import admin
from easy_select2 import select2_modelform
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

from .models import *


class FormResource(resources.ModelResource):

    class Meta:
        model = Form


@admin.register(Form)
class FormAdmin(ImportExportModelAdmin, ExportActionMixin,admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                        'name',
                        'submissionDeadline',
                        ('allowMultiple', 'applicationLimit', 'onSubmitAfterMax'),
                        'formHash',
                      ]
        }),
        ('Control Centre', {
            'fields': [
                        'admins',
                        ('isActive', 'enableCheckIn')
            ]
        }),
        ('RSVP Manager', {
            'fields': [
                'rsvpSubject',
                'rsvpMessage'
            ]
        }),
        ('Form Fields', {
            'fields': [
                        'formFields'
                      ]
        }),

    ]
    list_display = ('name', 'isActive', 'allowMultiple', 'enableCheckIn', 'applicationLimit')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2
    resource_class = FormResource


class ApplicationResource(resources.ModelResource):

    class Meta:
        model = Application


@admin.register(Application)
class ApplicationAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'name',
                ('form', 'submissionTime'),
                ('email', 'phone'),
                'hash', 'details'
            ]
        }),
        ('Form Fields', {
            'fields': [
                'formData'
            ]
        }),
        ('Status', {
            'fields': [
                ('status', 'rsvp', 'checkIn'),
                'checkInTime',
                'checkedInBy'
            ]
        }),

    ]
    list_display = ('name', 'form', 'status', 'submissionTime', 'rsvp', 'checkIn')
    list_filter = ('status', 'rsvp', 'checkIn')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2
    resource_class = ApplicationResource


