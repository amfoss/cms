import graphene
from graphql_jwt.decorators import login_required
from datetime import date, datetime, timedelta
from django.db.models import Avg
import dateutil.parser
from django.utils import timezone
from framework.api.user import UserBasicObj
from django.contrib.auth.models import User

from status.models import Log


class DailyStatusUpdateObj(graphene.ObjectType):
    timestamp = graphene.String()

    def resolve_timestamp(self, info):
        return self['timestamp']


class userDailyStatusUpdateObj(DailyStatusUpdateObj):
    user = graphene.Field(UserBasicObj)

    def resolve_user(self, info):
        return User.objects.values().get(id=self['member_id'])


class dailyStatusUpdateObj(graphene.ObjectType):
    date = graphene.types.datetime.Date()
    membersSend = graphene.Int()
    members = graphene.List(userDailyStatusUpdateObj)

    def resolve_membersSend(self, info):
        return len(self['logs'])

    def resolve_members(self, info):
        return self['logs'].values()


class clubStatusUpdatesObj(graphene.ObjectType):
    dailyLog = graphene.List(dailyStatusUpdateObj)

    def resolve_dailyLog(self, info):
        days = self.values_list('timestamp__date', flat=True).distinct()
        logs = []
        for day in days:

            logs.append({"date": day, "log": self['logs'].filter(timestamp__date=str(date))})
        return logs


class Query(object):
    clubStatusUpdates = graphene.Field(clubStatusUpdatesObj,
                                       startDate=graphene.types.datetime.Date(),
                                       endDate=graphene.types.datetime.Date()
                                       )

    @login_required
    def resolve_clubStatusUpdates(self, info, **kwargs):
        start = kwargs.get('startDate')
        end = kwargs.get('endDate')
        logs = Log.objects.all()
        if start is not None:
            logs = logs.filter(timestamp__gte=start)
        if end is not None:
            logs = logs.filter(timestamp__lte=end)
        return logs
