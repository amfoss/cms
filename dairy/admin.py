from django.contrib import admin
from datetime import datetime
from easy_select2 import select2_modelform
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    select2 = select2_modelform(Event, attrs={'width': '250px'})
    form = select2

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            obj.creationTime = datetime.now()
        obj.lastEditor = request.user
        obj.lastEditTime = datetime.now()
        obj.save()
