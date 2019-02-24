from django.contrib import admin
from .models import *
from activity.models import *

class sp_inline(admin.TabularInline):
    model = SocialProfile
    extra = 0

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

class wexp_inline(admin.StackedInline):
    model = WorkExperience
    fields  = (('organization', 'position'), ('start', 'end', 'location'),'projects','description')
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "projects":
            kwargs["queryset"] = Project.objects.filter(members=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

class eq_inline(admin.StackedInline):
    model = EducationalQualification
    fields = (('institution', 'title'), ('start','end'),('percentage','location'),('projects','certificate'),'description')
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "certificate":
            kwargs["queryset"] = Certificate.objects.filter(member=request.user)
        if db_field.name == "projects":
            kwargs["queryset"] = Project.objects.filter(members=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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

__all__ = ['eq_inline','sp_inline','wexp_inline']