import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import *


class StreamObj(DjangoObjectType):
    class Meta:
        model = Stream
        exclude_fields = ('id')


class TaskObj(DjangoObjectType):
    class Meta:
        model = Task


class TaskLogObj(DjangoObjectType):
    class Meta:
        model = TaskLog
        exclude_fields = ('id')


class Query(object):
    tasks = graphene.List(TaskObj)
    tasks_log = graphene.List(TaskObj, username=graphene.String(required=False), token=graphene.String(required=True))

    def resolve_tasks_log(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return TaskLog.objects.filter(member=user)
        else:
            return TaskLog.objects.all()
