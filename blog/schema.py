import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import *


class TagObj(DjangoObjectType):
    class Meta:
        model = Tag
        exclude_fields = ('id')


class CategoryObj(DjangoObjectType):
    class Meta:
        model = Category
        exclude_fields = ('id')


class PostObj(DjangoObjectType):
    class Meta:
        model = Post
        exclude_fields = ('id')


class ExternalPostObj(DjangoObjectType):
    class Meta:
        model = ExternalPost
        exclude_fields = ('id')


class Query(object):
    posts = graphene.List(PostObj, username=graphene.String(required=False))

    def resolve_posts(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return Post.objects.filter(author=user)
        else:
            return Post.objects.all()
