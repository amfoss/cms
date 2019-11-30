from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


class EventCheckInSlotInline(admin.TabularInline):
    model = CheckInSlot
    extra = 0
    select2 = select2_modelform(CheckInSlot, attrs={'width': '250px'})
    form = select2


class ParticipantCheckInInline(admin.TabularInline):
    model = CheckIn
    extra = 0
    select2 = select2_modelform(CheckIn, attrs={'width': '250px'})
    form = select2

