from django.contrib import admin
from easy_select2 import select2_modelform

from .models import *


@admin.register(Profile)
class StudentProfileAdmin(admin.ModelAdmin):
    fields = [
        ('user', 'rollNo'),
        ('admissionYear', 'branch', 'classSection'),
    ]
    list_display = ('user', 'admissionYear', 'branch')
    list_filter = ('admissionYear', 'branch')
    select2 = select2_modelform(Profile, attrs={'width': '250px'})
    form = select2

