from django.contrib import admin
from .models import Errors


@admin.register(Errors)
class ErrorsAdmin(admin.ModelAdmin):
    fields = [
        ('module', ),
        ('errorContent', 'timestamp'),
    ]

    list_display = ('module', 'timestamp')
