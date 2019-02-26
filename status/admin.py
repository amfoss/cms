from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    fields = ('date', ('thread', 'author'), 'subject', 'status')
    readonly_fields = ('date',)
    list_display = ('author', 'thread', 'date')
    list_filter = ('thread', 'author')
    search_fields = ['author__user', 'thread__name', 'subject', 'date']
    select2 = select2_modelform(Status, attrs={'width': '250px'})
    form = select2

@admin.register(StatusRegister)
class StatusRegisterAmdin(admin.ModelAdmin):
    list_display = ('member', 'date', 'status')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    fields= (('title', 'due_date'), ('status', 'tags'), ('assignees', 'team'), 'description', 'updates')
    select2 = select2_modelform(Task, attrs={'width': '250px'})
    form = select2


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    fields= (('title', 'date'), 'groups', 'description')
    select2 = select2_modelform(Notification, attrs={'width': '250px'})
    form = select2


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(TaskTag)
class TaskTagAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

