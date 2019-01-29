import graphene
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.types import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField

#
#       Mutations
#

class AtObj(graphene.ObjectType):
    id = graphene.String()

class RegisterAttendance(graphene.Mutation):
    class Arguments:
        session_start = graphene.types.datetime.DateTime(required=True)
        session_end = graphene.types.datetime.DateTime(required=True)
        token = graphene.String(required=True)

    Output = AtObj

    @login_required
    def mutate(self, info, session_start, session_end, token):
        user = User.objects.get(username=info.context.user)
        records = Attendance.objects.filter(session_start__date=session_start.date(), member=user)
        if not records:
            a = Attendance.objects.create(member=user, session_start=session_start, session_end=session_end)
            return AtObj(id=a.id)
        else:
            records.all().update(session_start=session_start, session_end=session_end)
            return AtObj(id=records[0].id)

class Mutation(object):
    RegisterAttendance = RegisterAttendance.Field()

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
        exclude_fields = ('id', 'user','links','experiences')

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
    profiles = graphene.List(ProfileObj,token=graphene.String(required=True))
    profile = graphene.Field(ProfileObj, username=graphene.String(required=True), token=graphene.String(required=True))

    attendance = DjangoFilterConnectionField(AttendanceObj)

    def resolve_profiles(self,info,**kwargs):
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