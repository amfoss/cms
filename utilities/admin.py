from django.contrib import admin
from .models import Mailer, Token
from datetime import datetime


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
            'fields': (('subject', 'form',), 'threadMessage',)
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
