from django.contrib import admin
from .models import *
from .inlines import *
from easy_select2 import select2_modelform


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = (EventCheckInSlotInline,)
    select2 = select2_modelform(Event, attrs={'width': '250px'})
    form = select2


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    inlines = (ParticipantCheckInInline,)
    select2 = select2_modelform(Participant, attrs={'width': '250px'})
    form = select2


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    readonly_fields = (id, )

    def has_module_permission(self, request):
        return False
