from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform

class StatusAdmin(admin.ModelAdmin):
    fields= ('date',('thread','author'),'subject','status')
    readonly_fields = ('date',)
    list_display = ('author', 'thread', 'date')
    list_filter = ('thread','author')
    search_fields = ['author__user', 'thread__name', 'subject', 'date']
    select2 = select2_modelform(Status, attrs={'width': '250px'})
    form = select2

class TaskAdmin(admin.ModelAdmin):
    fields= (('name','due_date'),('status','tags'),('assignees','team'),'updates')
    select2 = select2_modelform(Task, attrs={'width': '250px'})
    form = select2

class ThreadAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class TaskTagAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

class TaskStatusAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

admin.site.register(Thread,ThreadAdmin)
admin.site.register(TaskStatus,TaskStatusAdmin)
admin.site.register(TaskTag,TaskTagAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Status,StatusAdmin)

