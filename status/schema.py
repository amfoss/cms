import graphene
from graphql_jwt.decorators import login_required

from .models import *
from django.contrib.auth.models import User
from framework.api.user import UserBasicObj
from members.models import Group


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


class memberSentObj(graphene.ObjectType):
    member = graphene.Field(UserBasicObj)

    def resolve_member(self, info):
        return User.objects.values().get(id=self['member_id'])


class memberDidNotSendObj(graphene.ObjectType):
    member = graphene.Field(UserBasicObj)

    def resolve_member(self, info):
        return User.objects.values().get(id=self['member_id'])


class dailyStatusObj(graphene.ObjectType):
    date = graphene.types.datetime.Date()
    membersSent = graphene.List(memberSentObj)
    memberDidNotSend = graphene.List(memberDidNotSendObj)

    def resolve_date(self, info):
        return self

    def resolve_membersSent(self, info):
        return Message.objects.values().filter(date=self)

    def resolve_memberDidNotSend(self, info):
        groups = Group.objects.filter(statusUpdateEnabled=True).values('members__username')
        messages = Message.objects.values('member__username').filter(date=self)
        LogUsernames = []
        for i in messages:
            LogUsernames.append(i['member__username'])
        usernames = []
        for member in groups:
            username = member['members__username']
            if username not in LogUsernames:
                usernames.append(username)
        return usernames


class Query(graphene.ObjectType):
    getStatusUpdates = graphene.List(MessageObj, date=graphene.types.datetime.Date(required=True))
    getMemberStatusUpdates = graphene.List(MessageObj, username=graphene.String(required=True))
    dailyStatusUpdates = graphene.Field(
        dailyStatusObj,
        date=graphene.types.datetime.Date(required=True)
    )

    @login_required
    def resolve_getStatusUpdates(self, info, **kwargs):
        date = kwargs.get('date')
        return Message.objects.values().filter(date=date)

    @login_required
    def resolve_getMemberStatusUpdates(self, info, **kwargs):
        username = kwargs.get('username')
        return reversed(Message.objects.values().filter(member__username=username))

    @login_required
    def resolve_dailyStatusUpdates(self, info, **kwargs):
        return kwargs.get('date')