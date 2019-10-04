import graphene
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.types import DjangoObjectType
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from graphene_django.filter import DjangoFilterConnectionField
from datetime import date, datetime, timedelta
from django.conf import settings
from members.models import Group
import json

from django.utils import timezone

from .api.log import Query as logQuery

to_tz = timezone.get_default_timezone()


class AttendanceLogObj(graphene.ObjectType):
    id = graphene.String()


class LogAttendance(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        list = graphene.List(graphene.String)

    Output = AttendanceLogObj

    def mutate(self, info, username, password, list):
        time = datetime.now() - timedelta(minutes=5)
        recentLogsCount = Log.objects.filter(lastSeen__gte=time).count()

        user = User.objects.get(username=username)
        if user:
            if check_password(password, user.password):

                now = datetime.now().astimezone(to_tz)

                groups = Group.objects.filter(members__in=[user], attendanceEnabled=True)

                # check if member is part of any group, that has attendance enabled
                if groups.count() > 0:
                    for group in groups:
                        module = group.attendanceModule

                        # get details from thread
                        ssid = module.SSID

                        refreshInterval = module.seedRefreshInterval

                        # convert refresh interval to minutes
                        refreshMins = refreshInterval.seconds / 60

                        bypassSSID = 0
                        if recentLogsCount == 0:
                            newSSID = [i for i in list if i.startswith('amFOSS_')]
                            if len(newSSID) > 0:
                                bypassSSID = 1
                                module.SSID = newSSID[0]
                                module.seed = newSSID[0].strip('amFOSS_')
                                module.lastRefreshTime = datetime.now()
                                module.save()
                            else:
                                bypassSSID = 0

                        # check for matching ssid from list
                        if ssid in list or bypassSSID:

                            # Compute start time & end time for the current session

                            # Start Time =  Current Time - Current Minute % refreshInterval (in mins)
                            startTime = now - timedelta(
                                                    minutes=now.minute%refreshMins,
                                                    seconds=now.second,
                                                    microseconds=now.microsecond
                                                )

                            # End Time = Current Time + refreshInterval
                            endTime = startTime + refreshInterval

                            # create session object
                            session = {"start": startTime.isoformat(), "end": endTime.isoformat()}

                            # Checks if logs exist already for today
                            logs = Log.objects.filter(member=user, date=now.date())

                            # if logs exist for today, update existing log adding the current session
                            if logs.count() != 0:
                                log = logs[0]

                                prevSessions = log.sessions
                                prev = json.loads(prevSessions)

                                log.lastSeen = now

                                # check if session is not already marked
                                if prev[-1] != session:
                                    prev.append(session)
                                    log.sessions = json.dumps(prev)
                                    log.duration += refreshInterval

                                    # Add thread if not in days thread
                                    if module not in log.modules.all():
                                        log.modules.add(module)

                                log.save()

                                return AttendanceLogObj(id=log.id)

                            # else create a new log for the day
                            else:
                                log = Log.objects.create(
                                    member=user,
                                    date=now.date(),
                                    sessions=json.dumps([session]),
                                    duration=refreshInterval,
                                    lastSeen=now
                                )
                                log.modules.add(module)
                                log.save()
                                return AttendanceLogObj(id=log.id)
                        else:
                            raise Exception('Matching SSID Not Found')
                raise Exception('User not member of any group, or attendance for the group is not enabled')
            raise Exception('Wrong Password')
        raise Exception('User does not exist')

class Mutation(object):
    LogAttendance = LogAttendance.Field()

class attendanceModuleObj(graphene.ObjectType):
    SSID = graphene.String()
    lastRefreshTime = graphene.types.datetime.DateTime()
    lastRefresh = graphene.String()

    def resolve_lastRefreshTime(self, info):
        return self['lastRefreshTime'].astimezone(to_tz)

    def resolve_lastRefresh(self, info):
        time = self['lastRefreshTime'].astimezone(to_tz)
        return time.strftime("%H:%M:%S:%f")

class Query(logQuery):
    attendanceModule = graphene.Field(attendanceModuleObj, id=graphene.Int(required=True))

    @login_required
    def resolve_attendanceModule(self, info, **kwargs):
        id = kwargs.get('id')
        return Module.objects.values().get(id=id)

