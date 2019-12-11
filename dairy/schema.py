from datetime import datetime
import graphene
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from framework.api.user import UserBasicObj

from .models import *


class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['errorCode'] = code
        super().__init__(message)


class EventObj(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()

    creator = graphene.Field(UserBasicObj)
    creationTime = graphene.types.datetime.DateTime()
    lastEditor = graphene.Field(UserBasicObj)
    lastEditTime = graphene.types.datetime.DateTime()

    startTimestamp = graphene.types.datetime.DateTime()
    endTimestamp = graphene.types.datetime.DateTime()
    details = graphene.String()
    isAllDay = graphene.Boolean()

    def resolve_creator(self, info):
        try:
            user = User.objects.values().get(id=self['creator_id'])
        except ObjectDoesNotExist:
            user = None
        return user

    def resolve_lastEditor(self, info):
        try:
            user = User.objects.values().get(id=self['lastEditor_id'])
        except ObjectDoesNotExist:
            user = None
        return user


class eventObj(graphene.ObjectType):
    id = graphene.String()


class createEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        details = graphene.String()
        startTimestamp = graphene.DateTime()
        endTimestamp = graphene.DateTime()

    Output = eventObj

    @login_required
    def mutate(self, info, name, details, startTimestamp, endTimestamp):
        events = Event.objects.filter(name=name)
        if events.count() == 0:
            event = Event.objects.create(
                name=name,
                details=details,
                startTimestamp=startTimestamp,
                endTimestamp=endTimestamp,
                creator=info.context.user,
                creationTime=datetime.now(),
                lastEditTime=datetime.now(),
                lastEditor=info.context.user
            )
            event.save()
            return eventObj(id=event.id)
        else:
            raise APIException('Registered already with the same name',
                               code='ALREADY_REGISTERED')


class Query(object):
    viewEvents = graphene.List(
        EventObj,
        startDate=graphene.types.datetime.Date(required=True),
        endDate=graphene.types.datetime.Date(required=True)
    )

    @login_required
    def resolve_viewEvents(self, info, **kwargs):
        startDate = kwargs.get('startDate')
        endDate = kwargs.get('endDate')
        user = info.context.user
        if user.is_superuser:
            return Event.objects.values().filter((Q(startTimestamp__gte=startDate) & (Q(endTimestamp__lt=endDate) | Q(isAllDay=True))))
        else:
            return Event.objects.values().filter(
                (Q(startTimestamp__gte=startDate) & (Q(endTimestamp__lt=endDate) | Q(isAllDay=True)))
                & (Q(isPublic=True) | Q(creator=user) | Q(sharedGroups__members=user) | Q(admins=user))
            )


class Mutation(object):
    createEvent = createEvent.Field()