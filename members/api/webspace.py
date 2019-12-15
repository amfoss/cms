import graphene
from django.contrib.auth.models import User
from framework.api.user import UserBasicObj
from ..models import WebSpace


class WebSpaceObj(graphene.ObjectType):
    name = graphene.String()
    fileName = graphene.String()
    date = graphene.DateTime()
    user = graphene.Field(UserBasicObj)

    def resolve_name(self, info):
        return self['name']

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
        name = kwargs.get('name')
        if name is not None:
            return WebSpace.objects.values().get(name=name)
        raise Exception('Name is a required parameter')