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

    startTimestamp = graphene.types.datetime.Date()
    endTimestamp = graphene.types.datetime.Date()
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


class CertificateObj(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    eventName = graphene.String()
    fromDate = graphene.Date() 
    toDate = graphene.Date()
    issueDate = graphene.Date()

    def resolve_id(self, info):
        return self.uuid
        
    def resolve_eventName(self, info):
        e: Event = Event.objects.get(id=self.event_id)
        return e.name

    def resolve_fromDate(self, info):
        e: Event = Event.objects.get(id=self.event_id)
        return e.startTimestamp
    
    def resolve_toDate(self, info):
        e: Event = Event.objects.get(id=self.event_id)
        return e.endTimestamp

    def resolve_issueDate(self, info):
        return self.issue_date


class createEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        details = graphene.String()
        startTimestamp = graphene.Date()
        endTimestamp = graphene.Date()

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
        startDate=graphene.types.datetime.Date(required=True)
    )
    certVerify = graphene.Field(
        CertificateObj,
        id=graphene.ID(required=True)
    )
    certificates = graphene.List(
        CertificateObj,
        ids=graphene.List(graphene.ID, required=True)
    )

    @login_required
    def resolve_viewEvents(self, info, **kwargs):
        startDate = kwargs.get('startDate')
        user = info.context.user
        if user.is_superuser:
            return Event.objects.values().filter((Q(startTimestamp__gte=startDate) | Q(isAllDay=True)))
        else:
            return Event.objects.values().filter(
                (Q(startTimestamp__gte=startDate) | Q(isAllDay=True))
                & (Q(isPublic=True) | Q(creator=user) | Q(sharedGroups__members=user) | Q(admins=user))
            )

    def resolve_certVerify(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            try:
                c: Certificate = Certificate.objects.get(uuid=id)
                return c
            except Certificate.DoesNotExist:
                raise APIException('Certificate does not exist', code='INVALID_ID')
        raise APIException('ID is a required parameter', code='ID_REQUIRED')

    def resolve_certificates(self, info, **kwargs):
        ids = kwargs.get('ids')
        if ids is not None:
            output = Certificate.objects.filter(id__in=ids)
            if not output:
                raise APIException('No Certificates Found', 'NOT_FOUND')
            return output


class Mutation(object):
    createEvent = createEvent.Field()