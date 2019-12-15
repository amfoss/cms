import graphene
from django.contrib.auth.models import User
from framework.api.user import UserBasicObj
from ..models import WebSpace


class WebSpaceObj(graphene.ObjectType):
    fileName = graphene.String()
    date = graphene.DateTime()
    user = graphene.Field(UserBasicObj)

    def resolve_fileName(self, info):
        return self['file_name']

    def resolve_date(self, info):
        return self['date']

    def resolve_user(self, info):
        return User.objects.values().get(id=self['member_id'])


class Query(object):
    file = graphene.Field(
        WebSpaceObj,
        name=graphene.String(required=True)
    )

    def resolve_file(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return WebSpace.objects.values().get(user__username=username)
        raise Exception('Username is a required parameter')