from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    fields = [
        ('name', 'slug'),
        ('type', 'parents'),
        ('icon', 'color'),
        'description',
    ]
    select2 = select2_modelform(Task, attrs={'width': '250px'})
    form = select2


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields = [
        ('title', 'author'),
        ('date', 'stream'),
        ('difficulty', 'points'),
        'description',
    ]
    select2 = select2_modelform(Task, attrs={'width': '250px'})
    form = select2


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    fields = [
        ('member', 'task', 'status'),
        ('start_time', 'completion_time'),
        ('assigned_by', 'assign_time'),
        ('reviewers', 'points'),
        'proof',
    ]
    select2 = select2_modelform(TaskLog, attrs={'width': '250px'})
    form = select2



