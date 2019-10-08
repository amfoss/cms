from django.contrib import admin
from easy_select2 import select2_modelform

from .models import *


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
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


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'name',
                ('form', 'submissionTime'),
                ('email', 'phone'),
                'hash'
            ]
        }),
        ('Form Fields', {
            'fields': [
                'formData'
            ]
        }),
        ('Status', {
            'fields': [
                ('status', 'rsvp', 'checkIn')
            ]
        }),

    ]
    list_display = ('name', 'form', 'status', 'submissionTime', 'rsvp', 'checkIn')
    list_filter = ('status', 'rsvp', 'checkIn')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2
