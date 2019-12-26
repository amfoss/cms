from django.contrib import admin
from .models import Mailer


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
