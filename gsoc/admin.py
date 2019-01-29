from django.contrib import admin
from easy_select2 import select2_modelform
from .models import *

@admin.register(GSoC)
class GroupAdmin(admin.ModelAdmin):
    fields=(('member','status','organisation'),('year','proposal','topics'),('project','link'))
    search_fields = ['organisation', 'member']
    list_display = ('member', 'organisation')
    list_filter = ('member', 'organisation')
    select2 = select2_modelform(GSoC, attrs={'width': '250px'})
    form = select2
