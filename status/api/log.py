import graphene
from graphql_jwt.decorators import login_required
from datetime import date, datetime, timedelta
from django.db.models import Avg
import dateutil.parser
from django.utils import timezone
from framework.api.user import UserBasicObj
from django.contrib.auth.models import User

from status.models import Log
from members.models import Group

from members.api.group import GroupObj

to_tz = timezone.get_default_timezone()

class DailyStatusUpdateObj(graphene.ObjectType):
    timestamp = graphene.String()

    def resolve_timestamp(self, info):
        return self['timestamp'].astimezone(to_tz)


class userDailyStatusUpdateObj(DailyStatusUpdateObj):
    user = graphene.Field(UserBasicObj)

    def resolve_user(self, info):
        return User.objects.values().get(id=self['member_id'])


class userDailyStatusUpdateReportObj(userDailyStatusUpdateObj):
    lastSend = graphene.String()
    thisWeekCount = graphene.String()

    def resolve_lastSend(self, info):
        prev = Log.objects.filter(
            member__id=self['member_id'],
            date__lt=self['date'],
            thread__id=self['thread_id']
        )
        if prev.count() > 0:
            return prev.last().date
        else:
            return None

    def resolve_thisWeekCount(self, info):
        lastWeekDate = self['date'] - timedelta(days=7)
        return Log.objects.filter(
            member__id=self['member_id'],
            date__gte=lastWeekDate,
            thread__id=self['thread_id']
        ).count()


class groupDailyStatusUpdateObj(graphene.ObjectType):
    group = graphene.Field(GroupObj)
    membersSend = graphene.Int()
    members = graphene.List(userDailyStatusUpdateObj)

    def resolve_group(self, info):
        return self['group']

    def resolve_membersSend(self, info):
        return len(self['logs'])

    def resolve_members(self, info):
        return self['logs'].values()


class dailyStatusUpdateObj(graphene.ObjectType):
    date = graphene.types.datetime.Date()
    membersSend = graphene.Int()
    members = graphene.List(userDailyStatusUpdateObj)
    groups = graphene.List(groupDailyStatusUpdateObj)

    def resolve_membersSend(self, info):
        return len(self['logs'])

    def resolve_members(self, info):
        return self['logs'].values()

    def resolve_groups(self, info):
        groups = Group.objects.filter(statusUpdateEnabled=True)
        groupsData = []
        for group in groups:
            groupsData.append({"logs": self['logs'].filter(thread=group.thread), 'group': group})
        return groupsData


class clubStatusUpdatesObj(graphene.ObjectType):
    dailyLog = graphene.List(dailyStatusUpdateObj)

    def resolve_dailyLog(self, info):
        days = self.values_list('date', flat=True).distinct()
        logs = []
        for day in days:
            logs.append({"date": day, "logs": self.filter(date=day)})
        return logs


class dailyStatusUpdateReportObj(graphene.ObjectType):
    membersSend = graphene.Int()
    members = graphene.List(userDailyStatusUpdateReportObj)

    def resolve_membersSend(self, info):
        return len(self)

    def resolve_members(self, info):
        return self.values()


class Query(object):
    clubStatusUpdates = graphene.Field(clubStatusUpdatesObj,
                                       startDate=graphene.types.datetime.Date(),
                                       endDate=graphene.types.datetime.Date()
                                       )
    dailyStatusUpdateReport = graphene.Field(dailyStatusUpdateReportObj,
                                             date=graphene.types.datetime.Date(required=True),
                                             threadID=graphene.Int(required=True)
                                             )

    @login_required
    def resolve_clubStatusUpdates(self, info, **kwargs):
        start = kwargs.get('startDate')
        end = kwargs.get('endDate')
        logs = Log.objects.all()
        if start is not None:
            logs = logs.filter(date__gte=start)
        if end is not None:
            logs = logs.filter(date__lte=end)
        return logs

    @login_required
    def resolve_dailyStatusUpdateReport(self, info, **kwargs):
        date = kwargs.get('date')
        threadID = kwargs.get('threadID')
        return Log.objects.filter(date=date, thread__id=threadID)
