import graphene
import graphql_jwt
import attendance.schema
import activity.schema
import tasks.schema
import status.schema

from django.contrib.auth.models import User
from graphene_django_extras import DjangoObjectField, DjangoListObjectType, DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required


from members.schema import Query as MembersQuery, Mutation as membersMutation
from members.api.profile import ProfileObj
from members.api.group import GroupObj
from members.models import Profile, Group

from .api.user import UserBasicObj

class UserObj(UserBasicObj, graphene.ObjectType):
    profile = graphene.Field(ProfileObj)
    groups = graphene.List(GroupObj)

    def resolve_profile(self, info):
        return Profile.objects.values().get(user__username=self['username'])

    @login_required
    def resolve_groups(self, info):
        return Group.objects.filter(members__username=self['username']).values()


class Query(MembersQuery, attendance.schema.Query, activity.schema.Query, tasks.schema.Query, status.schema.Query, graphene.ObjectType):
    user = graphene.Field(UserObj, username=graphene.String(required=True))
    users = graphene.List(UserObj)

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.values().get(username=username)
        else:
            raise Exception('Username is a required parameter')

    def resolve_users(self, info):
        return User.objects.values().all()


class Mutation(membersMutation, attendance.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
