import graphene
import graphql_jwt
import members.schema
import attendance.schema
import activity.schema
import tasks.schema
import status.schema
from django.contrib.auth.models import User
from graphene_django_extras import DjangoObjectField, DjangoListObjectType, DjangoObjectType
from graphql_jwt.decorators import permission_required, login_required


class UserType(DjangoObjectType):
    class Meta:
        description = "Type definition for User Object"
        model = User
        exclude_fields = ('id', 'password')


class Query(members.schema.Query, activity.schema.Query, tasks.schema.Query, status.schema.Query, graphene.ObjectType):
    user = graphene.Field(UserType, username=graphene.String(required=False))

    @login_required
    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is None:
            username = info.context.user
        return User.objects.get(username=username)


class Mutation(members.schema.Mutation, attendance.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
