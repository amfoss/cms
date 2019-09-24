import graphene
import graphql_jwt
from datetime import date, datetime, timedelta
from django.utils import timezone
from graphql_jwt.decorators import permission_required, login_required
from django.contrib.auth.models import User

import attendance.schema
import activity.schema
import tasks.schema
import status.schema

from college.schema import Query as collegeQuery
from college.api.profile import StudentProfileObj
from college.models import Profile as CollegeProfile

from members.schema import Query as MembersQuery, Mutation as membersMutation
from members.api.profile import ProfileObj
from members.api.group import GroupObj
from members.models import Profile, Group

from attendance.models import Log

from .api.user import UserBasicObj


to_tz = timezone.get_default_timezone()


class UserObj(UserBasicObj, graphene.ObjectType):
    profile = graphene.Field(ProfileObj)
    groups = graphene.List(GroupObj)
    isInLab = graphene.Boolean()
    lastSeenInLab = graphene.types.datetime.DateTime()
    collegeProfile = graphene.Field(StudentProfileObj)

    def resolve_profile(self, info):
        return Profile.objects.values().get(user__username=self['username'])

    def resolve_collegeProfile(self, info):
        return CollegeProfile.objects.values().get(user__username=self['username'])

    @login_required
    def resolve_groups(self, info):
        return Group.objects.filter(members__username=self['username']).values()

    @login_required
    def resolve_isInLab(self, info):
        time = datetime.now() - timedelta(minutes=5)
        if Log.objects.filter(member__username=self['username'], lastSeen__gte=time).count() > 0:
            return True
        else:
            return False

    @login_required
    def resolve_lastSeenInLab(self, info):
        log = Log.objects.filter(member__username=self['username']).order_by('-lastSeen').values().first()
        return log['lastSeen'].astimezone(to_tz)


class Query(
    MembersQuery,
    collegeQuery,
    attendance.schema.Query,
    activity.schema.Query,
    tasks.schema.Query,
    status.schema.Query,
    graphene.ObjectType
):
    user = graphene.Field(UserObj, username=graphene.String(required=True))
    users = graphene.List(UserObj, sort=graphene.String(required=False))

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.values().get(username=username)
        else:
            raise Exception('Username is a required parameter')

    def resolve_users(self, info, **kwargs):
        sort = kwargs.get('sort')
        if sort is None:
            sort = 'username'
        return User.objects.values().all().order_by(sort)


class Mutation(membersMutation, attendance.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
