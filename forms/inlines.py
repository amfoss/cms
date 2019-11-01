from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


class FormSlotInline(admin.TabularInline):
    model = FormSlot
    extra = 0
    select2 = select2_modelform(FormSlot, attrs={'width': '250px'})
    form = select2

