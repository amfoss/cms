import graphene
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.types import DjangoObjectType
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from graphene_django.filter import DjangoFilterConnectionField
from datetime import date, datetime
from django.conf import settings


#
#       Mutations
#

class AtObj(graphene.ObjectType):
    id = graphene.String()

class LogAttendance(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        timestamp = graphene.types.datetime.DateTime(required=True)
        ssids = graphene.String(required=True)
        ip = graphene.String(required=True)


    Output = AtObj

    def mutate(self, info, username, password, timestamp, ssids, ip):
        user = User.objects.get(username=username)
        if check_password(password,user.password):
            al = AttendanceLog.objects.create(member=user, timestamp=timestamp, ssids=ssids, ip=ip)
            return AtObj(id=al.id)

class RecordLeaveToday(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        type = graphene.String(required=True)
        reason = graphene.String(required=True)
        bot_token = graphene.String(required=True)
        token = graphene.String(required=True)

    Output = AtObj

    def mutate(self, info, username, type, reason, bot_token, token):
        profile = Profile.objects.get(telegram_username=username)
        user = User.objects.get(username=profile.user.username)
        d =date.today()
        if bot_token == settings.TELEGRAM_BOT_TOKEN:
            lr = LeaveRecord.objects.create(member=user, start_date=d, end_date=d, type=type, reason=reason)
            return AtObj(id=lr.id)
        raise Exception('Invalid bot token')


class Mutation(object):
    LogAttendance = LogAttendance.Field()
    RecordLeaveToday = RecordLeaveToday.Field()


#
#       Queries
#

class PortalObj(DjangoObjectType):
    class Meta:
        model = Portal
        exclude_fields = ('id')


class SkillObj(DjangoObjectType):
    class Meta:
        model = Skill
        exclude_fields = ('id')


class OrganizationObj(DjangoObjectType):
    class Meta:
        model = Organization
        exclude_fields = ('id')

class ProfileObj(DjangoObjectType):
    class Meta:
        model = Profile
        exclude_fields = ('id', 'user', 'links', 'experiences')

    def resolve_id(self, info):
        raise Exception('You dont have access to view id of profile.')

class SocialProfileObj(DjangoObjectType):
    class Meta:
        model = SocialProfile

class WorkExperienceObj(DjangoObjectType):
    class Meta:
        model = WorkExperience

class AttendanceObj(DjangoObjectType):
    class Meta:
        model = Attendance
        exclude_fields = ('id',)
        filter_fields = {
            'member': ['exact'],
            'session_start': ['exact','gte']
        }
        interfaces = (graphene.relay.Node,)

class ResponsibilityObj(DjangoObjectType):
    class Meta:
        model = Responsibility
        exclude_fields = ('id')

class TeamObj(DjangoObjectType):
    class Meta:
        model = Team
        exclude_fields = ('id')

class MentorGroupObj(DjangoObjectType):
    class Meta:
        model = MentorGroup
        exclude_fields = ('id')


class Query(object):
    profiles = graphene.List(ProfileObj, token=graphene.String(required=True))
    profile = graphene.Field(ProfileObj, username=graphene.String(required=True), token=graphene.String(required=True))

    attendance = DjangoFilterConnectionField(AttendanceObj)

    def resolve_profiles(self, info, **kwargs):
        return Profile.objects.all()

    # def resolve_attendance(self,info,**kwargs):
    #     username = kwargs.get('username')
    #     if username is not None:
    #         user = User.objects.get(username=username)
    #         return Attendance.objects.get(user=user)
    #     raise Exception('Username is a required parameter')

    def resolve_profile(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return Profile.objects.get(user=user)
        raise Exception('Username is a required parameter')
