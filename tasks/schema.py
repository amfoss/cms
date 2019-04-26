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
    task = graphene.Field(TaskObj, id=graphene.String(required=True), token=graphene.String(required=True))
    tasks_log = graphene.List(TaskObj, username=graphene.String(required=False), token=graphene.String(required=True))

    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Task.objects.get(id=id)
        raise Exception('Task ID is a required parameter')

    def resolve_tasks_log(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return TaskLog.objects.filter(member=user)
        else:
            return TaskLog.objects.all()
