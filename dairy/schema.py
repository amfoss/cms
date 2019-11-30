import graphene
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from framework.api.user import UserBasicObj

from .models import *


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
