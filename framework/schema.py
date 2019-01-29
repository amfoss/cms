import graphene
import graphql_jwt
import members.schema
import blog.schema
import activity.schema
import status.schema
from django.contrib.auth.models import User
from graphene_django.types import DjangoObjectType

class UserObj(DjangoObjectType):
    class Meta:
        model = User
        exclude_fields = ('id','username','first_name','last_name','password','is_staff','is_active','is_superuser','last_login','date_joined','groups','email')


class Query(members.schema.Query, activity.schema.Query, blog.schema.Query, graphene.ObjectType):
    user = graphene.List(UserObj, username=graphene.String(required=True), token=graphene.String(required=True))

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.get(username=username)
        raise Exception('Username is a required parameter')



class Mutation(status.schema.Mutation, members.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
