from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


class sp_inline(admin.TabularInline):
    model = SocialProfile
    extra = 0
    select2 = select2_modelform(SocialProfile, attrs={'width': '250px'})
    form = select2

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.user != request.user:
            return False
        return True


__all__ = ['sp_inline', ]
