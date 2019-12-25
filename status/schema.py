from datetime import timedelta, date
from django.db.models import Count
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
        return User.objects.values().get(username=self)


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


class dailyStatusUpdateObj(graphene.ObjectType):
    date = graphene.types.datetime.Date()
    membersSentCount = graphene.Int()

    def resolve_date(self, info):
        return self['date']

    def resolve_membersSentCount(self, info):
        return len(self['message'])


class userStatusStatObj(graphene.ObjectType):
    user = graphene.Field(UserBasicObj)
    statusCount = graphene.String()

    def resolve_user(self, info):
        return User.objects.values().get(id=self['member'])


class clubStatusObj(graphene.ObjectType):
    memberStats = graphene.List(userStatusStatObj, order=graphene.String())
    dailyLog = graphene.List(dailyStatusUpdateObj)

    def resolve_memberStats(self, info, **kwargs):
        order = kwargs.get('order')
        if order is None:
            order = '-statusCount'
        return self['messages'].values('member').annotate(
            statusCount=Count('member')
        ).order_by(order)

    def resolve_dailyLog(self, info):
        sdate = self['start']
        delta = self['end'] - sdate
        days = []
        for i in range(delta.days + 1):
            days.append(sdate + timedelta(days=i))
        messages = []
        for day in days:
            messages.append({"date": day, "message": self['messages'].filter(date=day)})
        return messages


class Query(graphene.ObjectType):
    getStatusUpdates = graphene.List(MessageObj, date=graphene.types.datetime.Date(required=True))
    getMemberStatusUpdates = graphene.List(MessageObj, username=graphene.String(required=True))
    dailyStatusUpdates = graphene.Field(
        dailyStatusObj,
        date=graphene.types.datetime.Date(required=True)
    )
    clubStatusUpdate = graphene.Field(clubStatusObj,
                                      startDate=graphene.types.datetime.Date(required=True),
                                      endDate=graphene.types.datetime.Date()
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

    @login_required
    def resolve_clubStatusUpdate(self, info, **kwargs):
        start = kwargs.get('startDate')
        end = kwargs.get('endDate')
        messages = Message.objects.all()
        if start is not None:
            messages = messages.filter(date__gte=start)
        else:
            raise Exception('Start date required')
        if end is not None:
            messages = messages.filter(date__lte=end)
        else:
            end = date.today()
        data = {
            'messages': messages,
            'start': start,
            'end': end
        }
        return data
