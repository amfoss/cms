import graphene
from gallery.models import *
from framework.api.user import UserBasicObj
from django.db.models import F
from framework.api.APIException import APIException


class PhotoObj(graphene.ObjectType):
    caption = graphene.String()
    image = graphene.String()
    uploader = graphene.Field(UserBasicObj)
    date = graphene.Date()

    def resolve_caption(self, info):
        return self['caption']

    def resolve_image(self, info):
        return self['image']

    def resolve_uploader(self, info):
        return User.objects.values().get(id=self['uploader_id'])

    def resolve_date(self, info):
        return self['date']


class AlbumObj(graphene.ObjectType):
    title = graphene.String()
    uploader = graphene.Field(UserBasicObj)
    date = graphene.Date()
    description = graphene.String()
    photos = graphene.List(PhotoObj)

    def resolve_title(self, info):
        return self['title']

    def resolve_uploader(self, info):
        return User.objects.values().get(id=self['uploader_id'])

    def resolve_date(self, info):
        return self['date']

    def resolve_description(self, info):
        return self['description']

    @graphene.resolve_only_args
    def resolve_photos(self):
        return Album.objects.values().annotate(
            caption=F('photos__caption'),
            image=F('photos__image'),
            date=F('photos__date'),
            uploader=F('photos__uploader')
        ).filter(id=self['id'])


class Query(graphene.ObjectType):
    photos = graphene.List(PhotoObj)
    photo = graphene.Field(PhotoObj, caption=graphene.String())
    albums = graphene.List(AlbumObj)
    album = graphene.Field(AlbumObj, title=graphene.String())

    def resolve_photos(self, info):
        return reversed(Photo.objects.values().all().order_by('date'))

    def resolve_photo(self, info, **kwargs):
        caption = kwargs.get('caption')
        if caption is not None:
            return Photo.objects.values().get(caption=caption)
        else:
            raise APIException('Caption is required',
                               code='CAPTION_IS_REQUIRED')

    def resolve_albums(self, info):
        return Album.objects.values().all().order_by('date')

    def resolve_album(self, info, **kwargs):
        title = kwargs.get('title')
        if title is not None:
            return Album.objects.values().get(title=title)
        else:
            raise APIException('Title is required',
                               code='TITLE_IS_REQUIRED')


schema = graphene.Schema(query=Query)

