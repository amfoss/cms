from django.contrib import admin
from .models import Password
from easy_select2 import select2_modelform


@admin.register(Password)
class PasswordAdmin(admin.ModelAdmin):
    fields = [('name', 'login_name', 'password'), ('admins', 'url'), 'details']

    select2 = select2_modelform(Password, attrs={'width': '500px'})
    form = select2
    list_display = ['name', 'login_name', 'url']
