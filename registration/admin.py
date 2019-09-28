from django.contrib import admin
from easy_select2 import select2_modelform

from .models import *


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'form', 'submissionTime', 'email', 'phone')
    select2 = select2_modelform(Form, attrs={'width': '250px'})
    form = select2
