import graphene
from graphene_django.types import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField

class LanguageNode(DjangoObjectType):
    class Meta:
        model = Language
        filter_fields = {
            'name': ['exact',],
        }
        interfaces = (graphene.relay.Node,)
        exclude_fields = ('ID',)

class LanguageInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class CreateLanguage(graphene.relay.ClientIDMutation):
    class Input:
        language = graphene.Argument(LanguageInput)

    language = graphene.Field(LanguageNode)

    @classmethod
    def mutate_and_get_payload(root, info, **input):
        language_data = args.get('language')
        language = Language()
        new_language = update_create_instance(language, language_data)

        return cls(language=new_language)

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

class Mutation(object):
    create_language = CreateLanguage.Field()

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