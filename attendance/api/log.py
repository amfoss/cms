import graphene
from graphql_jwt.decorators import login_required
from django.db.models import F
from datetime import date, datetime, timedelta
from django.utils import timezone
from framework.api.user import UserBasicObj
from django.contrib.auth.models import User

from ..models import Log
from members.models import Group


class attendanceStatObj(graphene.ObjectType):
    count = graphene.Int()
    members = graphene.List(UserBasicObj)

    def resolve_members(self, info):
        return User.objects.values().filter(username__in=self['members'])

class liveAttendanceObj(graphene.ObjectType):
    membersPresent = graphene.Field(attendanceStatObj)
    membersAbsent = graphene.Field(attendanceStatObj)

    def resolve_membersPresent(self, info):
        count = len(self)
        return {'count': count, 'members': self}

    def resolve_membersAbsent(self, info):
        groups = Group.objects.filter(attendanceEnabled=True).values('members__username')
        usernames = []
        for member in groups:
            username = member['members__username']
            if username not in self:
                usernames.append(username)
        count = len(usernames)
        return {'count': count, 'members': usernames}


class Query(object):
    liveAttendance = graphene.Field(liveAttendanceObj)

    @login_required
    def resolve_liveAttendance(self, info):
        time = datetime.now() - timedelta(minutes=5)
        logs = Log.objects.annotate(
            username=F('member__username')
        ).filter(lastSeen__gte=time).values('username')
        u = []
        for i in logs:
            u.append(i['username'])
        return u
