import graphene
from .models import *
from framework.api.user import UserBasicObj
from django.db.models import F
from framework.api.APIException import APIException


class CategoryObj(graphene.ObjectType):
    name = graphene.String()
    author = graphene.Field(UserBasicObj)

    def resolve_name(self, info):
        return self['name']

    def resolve_author(self, info):
        return User.objects.values().get(id=self['author_id'])


class TagObj(graphene.ObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self['name']


class NewsObj(graphene.ObjectType):
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    author = graphene.Field(UserBasicObj)
    date = graphene.Date(required=True)
    category = graphene.Field(CategoryObj)
    tags = graphene.List(TagObj)
    pinned = graphene.Boolean()
    description = graphene.String(required=True)
    cover = graphene.String(required=True)

    def resolve_title(self, info):
        return self['title']

    def resolve_slug(self, info):
        return self['slug']

    def resolve_author(self, info):
        return User.objects.values().get(id=self['author_id'])

    def resolve_date(self, info):
        return self['date']

    def resolve_pinned(self, info):
        return self['pinned']

    def resolve_category(self, info):
        return Category.objects.values().get(id=self['category_id'])

    @graphene.resolve_only_args
    def resolve_tags(self):
        return News.objects.values().annotate(
            name=F('tags__name'),
        ).filter(id=self['id'])

    def resolve_cover(self, info):
        return self['cover']


class Query(graphene.ObjectType):
    news = graphene.List(NewsObj)
    getNews = graphene.Field(NewsObj, slug = graphene.String(required=True))
    tags = graphene.List(TagObj)
    categories = graphene.List(CategoryObj)
    
    def resolve_news(self, info):
        return reversed(News.objects.values().all().order_by('date'))

    def resolve_getNews(self, info, **kwargs):
        slug = kwargs.get('slug')
        if slug is not None:
            return News.objects.values().get(slug=slug)
        else:
            raise APIException('Slug is required',
                               code='SLUG_IS_REQUIRED')

    def resolve_tags(self, info):
        return Tag.objects.values().all()

    def resolve_categories(self, info):
        return Category.objects.values().all()


schema = graphene.Schema(query=Query)
