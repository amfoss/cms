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
                        ('isActive', 'allowMultiple'),
                        ('applicationLimit', 'onSubmitAfterMax'),
                        'formHash',
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
    list_display = ('name', 'isActive', 'allowMultiple', 'applicationLimit')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'status', 'submissionTime', 'rsvp', 'email', 'phone')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2
