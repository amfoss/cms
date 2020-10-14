from django.contrib import admin
from .models import Mailer, Token, Emails
from datetime import datetime
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


class EmailResource(resources.ModelResource):
    class Meta:
        model = Emails


@admin.register(Emails)
class EmailAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'category')
        }),
        ('Emails', {
            'fields': ('email',)
        })
    )

    list_display = ('name', 'category', 'email')


@admin.register(Mailer)
class MailerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        ('Timings', {
            'fields': (('generationEmailTime', 'generationEmailDate'),)
        }),
        ('Mailing', {
            'fields': (('subject', 'form', 'category'), 'threadMessage',)
        }),
    )

    list_display = ('name', 'form', 'generationEmailDate', 'generationEmailTime')


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Token', {
            'fields': (('key', 'value'),)
        }),
        ('History', {
            'fields': (('creator', 'creationTime'), ('lastEditor', 'lastEditTime'))
        }),
    )

    list_display = ('key', 'lastEditor', 'lastEditTime')

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
            obj.creationTime = datetime.now()
        obj.lastEditor = request.user
        obj.lastEditTime = datetime.now()
        obj.save()
