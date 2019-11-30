import graphene
from graphene_django.types import DjangoObjectType
from .models import *


class StreamObj(DjangoObjectType):
    class Meta:
        model = Stream
        exclude_fields = ('id',)


class TaskObj(DjangoObjectType):
    class Meta:
        model = Task


class TaskLogObj(DjangoObjectType):
    class Meta:
        model = TaskLog
        exclude_fields = ('id',)


class streamProgressObj(graphene.ObjectType):
    progress = graphene.Float()
    tasksCompleted = graphene.Int()
    tasksInProgress = graphene.Int()
    tasksPending = graphene.Int()


class taskProgressObj(graphene.ObjectType):
    status = graphene.String()
    isComplete = graphene.Boolean()
    start = graphene.String()
    submission = graphene.String()
    assignTime = graphene.String()
    assigner = graphene.String()


class Query(object):
    stream = graphene.Field(StreamObj, slug=graphene.String(required=True))
    streams = graphene.List(StreamObj,
                            stream_type=graphene.String(required=False),
                            hasParent=graphene.Boolean(required=False),
                            parent=graphene.Boolean(required=False)
                            )

    streamProgress = graphene.Field(streamProgressObj,
                                    slug=graphene.String(required=True),
                                    username=graphene.String(required=True),
                                    token=graphene.String(required=True)
                                    )

    task = graphene.Field(TaskObj, id=graphene.String(required=True))
    tasks = graphene.List(TaskObj,
                          stream=graphene.String(required=False),
                          max_points=graphene.Int(required=False),
                          min_points=graphene.Int(required=False),
                          max_difficulty=graphene.Int(required=False),
                          min_difficulty=graphene.Int(required=False),
                          )
    tasks_log = graphene.List(TaskObj,
                              username=graphene.String(required=False),
                              token=graphene.String(required=True)
                              )
    taskProgress = graphene.Field(taskProgressObj,
                                    id=graphene.Int(required=True),
                                    username=graphene.String(required=True),
                                    token=graphene.String(required=True)
                                 )


    def resolve_stream(self, info, **kwargs):
        slug = kwargs.get('slug')
        if slug is not None:
            return Stream.objects.get(slug=slug)
        raise Exception('Stream Slug is a required parameter')

    def resolve_streams(self, info, **kwargs):
        stream_type = kwargs.get('stream_type')
        hasParent = kwargs.get('hasParent')
        parent = kwargs.get('parent')
        streams = Stream.objects.all()
        if stream_type is not None:
            streams = streams.filter(type=stream_type)
        if hasParent is not None:
            streams = streams.filter(parent__isnull=not hasParent)
        elif parent is not None:
            parent_obj = Stream.objects.get(slug=parent)
            streams = streams.filter(parent=parent_obj)
        return streams

    def resolve_streamProgress(self, info, **kwargs):
        slug = kwargs.get('slug')
        username = kwargs.get('username')
        if slug is not None:
            stream = Stream.objects.get(slug=slug)
            user = User.objects.get(username=username)
            tasksCount = Task.objects.filter(stream=stream).count()
            tlogs = TaskLog.objects.filter(task__stream=stream, member=user)
            logsCount = tlogs.filter(status=4).count()
            tasksInProgress = tlogs.count()
            if tasksCount > 0:
                progress = float(logsCount / tasksCount)
                tasksPending = tasksCount - logsCount
            else:
                progress = 0
                tasksPending = 0
            return streamProgressObj(progress=progress, tasksInProgress=tasksInProgress, tasksCompleted=logsCount, tasksPending=tasksPending)
        raise Exception('Stream Slug is a required parameter')

    def resolve_tasks(self, info, **kwargs):
        stream = kwargs.get('stream')
        max_points = kwargs.get('max_points')
        min_points = kwargs.get('min_points')
        max_difficulty = kwargs.get('max_difficulty')
        min_difficulty = kwargs.get('min_difficulty')

        tasks = Task.objects.all()
        if stream is not None:
            s = Stream.objects.get(slug=stream)
            tasks = Task.objects.filter(stream=s)
        if max_points is not None:
            tasks = tasks.filter(points__lte=max_points)
        if min_points is not None:
            tasks = tasks.filter(points__gte=min_points)
        if max_difficulty is not None:
            tasks = tasks.filter(difficulty__lte=max_difficulty)
        if min_difficulty is not None:
            tasks = tasks.filter(difficulty__gte=min_difficulty)
        return tasks

    def resolve_task(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Task.objects.get(id=id)
        raise Exception('Task ID is a required parameter')

    def resolve_taskProgress(self, info, **kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')
        if id is not None:
            log = TaskLog.objects.filter(member__username=username, task_id__exact=id)
            if log.count() > 0:
                status = log[0].status
                if int(status) == 4:
                    isComplete = True
                else:
                    isComplete = False
                start = log[0].start_time
                submission = log[0].completion_time
                assignTime = log[0].assign_time
                assigner = log[0].assigned_by.username
            return taskProgressObj(status=status,
                                   isComplete=isComplete,
                                   start=start,
                                   submission=submission,
                                   assignTime=assignTime,
                                   assigner=assigner)
        raise Exception('Task ID is a required parameter')

    def resolve_tasks_log(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return TaskLog.objects.filter(member=user)
        else:
            return TaskLog.objects.all()
