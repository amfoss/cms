from django.contrib import admin
from .models import *
from easy_select2 import select2_modelform


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 0

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = [
                ('name', 'slug'),
                ('members', 'album'),
                ('tagline', 'topics'),
                ('published', 'cover'),
                'detail',
                'featured',
            ]
    list_display = ('name', 'featured', 'published')
    inlines = (ProjectLinkInline,)
    select2 = select2_modelform(Project, attrs={'width': '250px'})
    form = select2

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('featured')
        return fields

    def get_queryset(self, request):
        qs = super(ProjectAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(members=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user not in obj.members.all():
            return False
        return True


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    fields = [
                'title',
                ('member', 'issuer'),
                ('date', 'attachment'),
                'topics'
              ]
    select2 = select2_modelform(Certificate, attrs={'width': '250px'})
    form = select2

    def get_queryset(self, request):
        qs = super(CertificateAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(member=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = [
                ('name', 'issuer'),
                ('member', 'certificate'),
                ('topics', 'url')
             ]
    select2 = select2_modelform(Course, attrs={'width': '250px'})
    form = select2


    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(member=request.user)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.member != request.user:
            return False
        return True