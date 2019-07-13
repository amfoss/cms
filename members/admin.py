from django.contrib import admin
from .models import *
from activity.models import *
from .inlines import *
from easy_select2 import select2_modelform
from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, DurationField
import datetime

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                        'user',
                        ('first_name', 'last_name', 'avatar'),
                        ('email', 'phone', 'telegram_id'),
                      ]
        }),
        ('Additional Details', {
            'fields': [
                        ('roll_number', 'batch', 'birthday'),
                        ('resume', 'system_no', 'typing_speed'),
                        ('location', 'languages'),
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
    inlines = (sp_inline, wexp_inline, eq_inline)
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

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    fields  = (('member', 'timestamp','ip'), 'ssids')
    list_display = ('member', 'timestamp', 'ssids', 'ip')
    list_filter = ('member', 'timestamp')
    select2 = select2_modelform(AttendanceLog, attrs={'width': '250px'})
    form = select2

class DurationFilter(admin.SimpleListFilter):
    title='Duration'
    parameter_name='calculated_duration'

    def lookups(self, request, queryset):
        return(
            ('1','More than 3 hours'),
            ('2','Less than 3 hours'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(xduration__gt=datetime.timedelta(hours=3))
        elif value == '2':
            return queryset.exclude(xduration__gt=datetime.timedelta(hours=3))
        return queryset

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    fields = ('member', ('session_start', 'session_end'),)
    list_display = ('member', 'session_start', 'session_end', 'calculated_duration')
    list_filter = ('member', 'session_start', DurationFilter)

    def calculated_duration(self, obj):
        return obj.xduration
    calculated_duration.admin_order_field = 'xduration'
    calculated_duration.short_description = ('duration')

    def get_queryset(self, request):
        qs = super(AttendanceAdmin, self).get_queryset(request)
        qs = qs.annotate(xduration=ExpressionWrapper(F('session_end')-F('session_start'), output_field=DurationField())).order_by('xduration')
        return qs

    select2 = select2_modelform(Attendance, attrs={'width': '250px'})
    form = select2


@admin.register(LeaveRecord)
class LeaveRecordAdmin(admin.ModelAdmin):
    fields = [
                ('member', 'type'),
                ('start_date', 'end_date'),
                'reason'
             ]
    list_display = ('member', 'type', 'start_date', 'end_date')
    list_filter = ('member', 'type')
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


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    search_fields = ['title', 'members']
    list_display = ('title', 'thread')
    list_filter = ('title','members')
    select2 = select2_modelform(Responsibility, attrs={'width': '250px'})
    form = select2


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name', 'members']
    list_display = ('name', 'thread')
    list_filter = ('name', 'members')
    select2 = select2_modelform(Team, attrs={'width': '250px'})
    form = select2


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    fields = (('name', 'description'), 'members')
    search_fields = ['name', 'members']
    list_display = ('name', 'description')
    list_filter = ('name', 'members')
    select2 = select2_modelform(Group, attrs={'width': '250px'})
    form = select2


@admin.register(MentorGroup)
class MentorGroupAdmin(admin.ModelAdmin):
    search_fields = ['mentor', 'mentees']
    list_display = ('mentor',)
    list_filter = ('mentor',)
    select2 = select2_modelform(MentorGroup, attrs={'width': '250px'})
    form = select2


@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
