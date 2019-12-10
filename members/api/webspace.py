import graphene
from ..models import WebSpace


class WebSpaceObj(graphene.ObjectType):
    name = graphene.String()
    fileName = graphene.String()
    date = graphene.DateTime()

    def resolve_name(self, info):
        return self['name']

    def resolve_fileName(self, info):
        return self['file_name']

    def resolve_date(self, info):
        return self['date']


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