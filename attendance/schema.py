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
        user = User.objects.get(username=username)
        if user:
            if check_password(password, user.password):

                now = datetime.now().astimezone(to_tz)

                groups = Group.objects.filter(members__in=[user], attendanceEnabled=True)

                # check if member is part of any group, that has attendance enabled
                if groups.count() > 0:
                    for group in groups:
                        thread = group.attendanceThread

                        # get details from thread
                        ssid = thread.SSID

                        refreshInterval = thread.seedRefreshInterval

                        #convert refresh interval to minutes
                        refreshMins = refreshInterval.seconds / 60

                        # check for matching ssid from list
                        if ssid in list:

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
                            session = { "start": startTime.isoformat(), "end": endTime.isoformat() }

                            # Checks if logs exist already for today
                            logs = Log.objects.filter(member=user, date=now.date())

                            # if logs exist for today, update existing log adding the current session
                            if logs.count() != 0:
                                log = logs[0]

                                prevSessions = log.sessions
                                prev = json.loads(prevSessions)

                                # check if session is not already marked
                                if prev[-1] != session:
                                    prev.append(session)
                                    log.sessions = json.dumps(prev)
                                    log.duration += refreshInterval

                                    ## Add thread if not in days thread
                                    if thread not in log.threads.all():
                                        log.threads.add(thread)

                                    log.save()

                                return AttendanceLogObj(id=log.id)

                            # else create a new log for the day
                            else:
                                log = Log.objects.create(
                                    member=user,
                                    date=now.date(),
                                    sessions=json.dumps([session]),
                                    duration=refreshInterval,
                                )
                                log.threads.add(thread)
                                log.save()
                                return AttendanceLogObj(id=log.id)
                        else:
                            raise Exception('Matching SSID Not Found')
                        raise Exception('interval should be processed.')
                raise Exception('User not member of any group, or attendance for the group is not enabled')
            raise Exception('Wrong Password')
        raise Exception('User does not exist')

class Mutation(object):
    LogAttendance = LogAttendance.Field()