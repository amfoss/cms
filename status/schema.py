import graphene
from .models import *
from django.contrib.auth.models import User
from framework.api.user import UserBasicObj


class MessageObj(graphene.ObjectType):
    message = graphene.String()
    member = graphene.Field(UserBasicObj)
    date = graphene.Date()
    timestamp = graphene.DateTime()

    def resolve_message(self, info):
        return self['message']

    def resolve_member(self, info):
        return User.objects.values().get(id=self['member_id'])

    def resolve_timestamp(self, info):
        return self['timestamp']


class Query(graphene.ObjectType):
    getStatusUpdates = graphene.List(MessageObj, date=graphene.types.datetime.Date(required=True))

    def resolve_getStatusUpdates(self, info, **kwargs):
        date = kwargs.get('date')
        return Message.objects.values().filter(date=date)
