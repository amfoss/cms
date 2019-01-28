from django.contrib import admin
from .models import *
from activity.models import *

class sp_inline(admin.TabularInline):
    model = SocialProfile
    extra = 0

class wexp_inline(admin.StackedInline):
    model = WorkExperience
    fields  = (('organization', 'position'), ('start', 'end', 'location'),'projects','description')
    extra = 0

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "projects":
            kwargs["queryset"] = Project.objects.filter(members=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

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
