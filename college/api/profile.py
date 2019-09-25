import graphene
from ..models import Profile
from graphql_jwt.decorators import login_required


class StudentProfileObj(graphene.ObjectType):
    username = graphene.String()
    rollNo = graphene.String()
    admissionYear = graphene.Int()
    branch = graphene.String()
    classSection = graphene.String()

    @login_required
    def resolve_rollNo(self, info):
        return self['rollNo']

    @login_required
    def resolve_classSection(self, info):
        return self['classSection']


class Query(object):
    collegeProfile = graphene.Field(
        StudentProfileObj,
        username=graphene.String(required=True)
    )
    collegeProfiles = graphene.List(StudentProfileObj)

    def resolve_collegeProfile(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            profile = Profile.objects.values().get(user__username=username)
            return profile
        raise Exception('Username is a required parameter')

    def resolve_collegeProfiles(self, info, **kwargs):
        return Profile.objects.values().all()


