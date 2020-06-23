import graphene
from framework.api.user import UserBasicObj
from events.models import *
from framework.api.APIException import APIException
from gallery.models import Album
from gallery.schema import AlbumObj


class EventsObj(graphene.ObjectType):
    title = graphene.String()
    slug = graphene.String()
    content = graphene.String()
    creator = graphene.Field(UserBasicObj)
    date = graphene.DateTime()
    album = graphene.Field(AlbumObj)

    def resolve_title(self, info):
        return self['name']
    
    def resolve_slug(self, info):
        return self['slug']

    def resolve_content(self, info):
        return self['content']

    def resolve_creator(self, info):
        return User.objects.values().get(id=self['creator_id'])
    
    def resolve_date(self, info):
        return self['date']

    def resolve_album(self, info):
        return Album.objects.values().get(id=self['album_id'])


class Query(graphene.ObjectType):
    events = graphene.List(EventsObj)
    event = graphene.Field(EventsObj, slug=graphene.String(required=True))

    def resolve_events(self, info):
        return Event.objects.values().all()

    def resolve_event(self, info, **kwargs):
        slug = kwargs.get('slug')
        if slug is not None:
            return Event.objects.values().get(slug=slug)
        else:
            raise APIException('Slug is required',
                               code='SLUG_IS_REQUIRED')


schema = graphene.Schema(query=Query)
