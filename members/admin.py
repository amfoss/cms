from django.contrib import admin
from .models import *
from .inlines import *
from easy_select2 import select2_modelform
from django.contrib.auth.models import User

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin, ExportActionMixin, DefaultUserAdmin):
    resource_class = UserResource
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileResource(resources.ModelResource):

    class Meta:
        model = Profile


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'user',
                ('first_name', 'last_name', 'profile_pic'),
                ('email', 'phone', 'customEmail'),
                ('telegram_id', 'discord_id', 'githubUsername', 'gitlabUsername')
            ]
        }),
        ('Additional Details', {
            'fields': [
                ('role', ),
                ('roll_number', 'batch', 'birthday'),
                ('resume', 'system_no', 'typing_speed'),
                ('location', 'languages', 'displayInWebsite'),
                ('cover', 'accent', 'tagline'),
                'about'
            ]
        }),
        ('Interests & Expertise', {
            'fields': [
                ('interests', 'expertise'),
            ]
        }),

    ]
    inlines = (sp_inline, )
    list_display = ('first_name', 'last_name', 'batch')
    list_filter = ('batch',)
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'batch']
    select2 = select2_modelform(Profile, attrs={'width': '250px'})
    form = select2

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(username=request.user.username)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# class DurationFilter(admin.SimpleListFilter):
#     title='Duration'
#     parameter_name='calculated_duration'
#
#     def lookups(self, request, queryset):
#         return(
#             ('1','More than 3 hours'),
#             ('2','Less than 3 hours'),
#         )
#
#     def queryset(self, request, queryset):
#         value = self.value()
#         if value == '1':
#             return queryset.filter(xduration__gt=datetime.timedelta(hours=3))
#         elif value == '2':
#             return queryset.exclude(xduration__gt=datetime.timedelta(hours=3))
#         return queryset

class LeaveRecordResource(resources.ModelResource):

    class Meta:
        model = LeaveRecord


@admin.register(LeaveRecord)
class LeaveRecordAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = [
        ('member', 'approver', 'type'),
        ('start_date', 'end_date'),
        'reason'
    ]
    list_display = ('member', 'approver', 'type', 'start_date', 'end_date')
    list_filter = ('type',)
    select2 = select2_modelform(LeaveRecord, attrs={'width': '250px'})
    form = select2

    def get_queryset(self, request):
        qs = super(LeaveRecordAdmin, self).get_queryset(request)
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


class ResponsibilityResource(resources.ModelResource):

    class Meta:
        model = Responsibility


@admin.register(Responsibility)
class ResponsibilityAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    search_fields = ['title', 'members']
    list_display = ('title', 'thread')
    select2 = select2_modelform(Responsibility, attrs={'width': '250px'})
    form = select2


class GroupResource(resources.ModelResource):

    class Meta:
        model = Group


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'admins'),
                'members'
            )
        }),
        ('Attendance Management', {
            'fields': (
                'attendanceEnabled',
                'attendanceModule',
            )
        }),
        ('Status Update Management', {
            'fields': (
                'statusUpdateEnabled',
                ('thread',),
            )
        }),
        ('Telegram Integration', {
            'fields': (('telegramBot', 'telegramGroup'),)
        }),
        ('Discord Integration', {
            'fields': (('discordBot', 'discordGroup', 'discordChannel'),)
        }),
    )
    search_fields = ['name', 'members']
    list_display = ('name', 'members_count', 'attendanceEnabled', 'statusUpdateEnabled')
    select2 = select2_modelform(Group, attrs={'width': '800px', 'max-width': '100%'})
    form = select2

    def members_count(self, obj):
        return obj.members.all().count()

    members_count.verbose_name = 'No. of Mentees'


class MentorGroupResource(resources.ModelResource):

    class Meta:
        model = MentorGroup


@admin.register(MentorGroup)
class MentorGroupAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    search_fields = ['mentor', 'mentees']
    list_filter = ('sendReport', 'forwardStatusUpdates')
    list_display = ('mentor', 'sendReport', 'forwardStatusUpdates', 'mentees_count', 'mentees_display')
    select2 = select2_modelform(MentorGroup, attrs={'width': '250px'})
    form = select2

    def mentees_count(self, obj):
        return obj.mentees.all().count()

    mentees_count.verbose_name = 'No. of Mentees'

    def mentees_display(self, obj):
        return ", ".join([
            mentee.username for mentee in obj.mentees.all()
        ])

    mentees_display.verbose_name = 'Mentees'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    fields = [
                ('name', 'slug'),
                'members',
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


class WebspaceResource(resources.ModelResource):

    class Meta:
        model = WebSpace


@admin.register(WebSpace)
class WebSpaceAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fields = ['name', 'user', ('file_name',  'date')]

    list_display = ('name', 'user', 'date',)


@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):
    fields = ['name', ('icon', 'color')]

    list_display = ('name', 'icon', 'color')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    fields = ['name', ('type', 'icon')]

    list_display = ('name', 'type')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
