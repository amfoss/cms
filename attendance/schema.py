import graphene
from graphql_jwt.decorators import permission_required, login_required
from graphene_django.types import DjangoObjectType
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from graphene_django.filter import DjangoFilterConnectionField
from datetime import date, datetime
from django.conf import settings
import json


class AttendanceLogObj(graphene.ObjectType):
    id = graphene.String()

class LogAttendance(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        time = graphene.types.datetime.DateTime(required=True)
        secret = graphene.String(required=True)
        list = graphene.String(required=True)

    Output = AttendanceLogObj

    def mutate(self, info, username, password, time, secret, list):
        user = User.objects.get(username=username)
        if user:
            if check_password(password, user.password):
                # now = datetime.now()
                #
                # # minMin = now.minute - min.minute % 10;
                # # min =
                #
                # print(secret)
                # print(list)
                #
                day = time.date()
                # diff = end - start
                # session = { "start" : start.isoformat(), "end": end.isoformat() }

                session = { "time": time.isoformat() }
                session = json.dumps(session)
                logs = Log.objects.filter(member=user, date=day)
                if logs.count() != 0:
                    log = logs[0]
                    sessions = log.sessions[:-1] + ',' + session + ']'
                    log.sessions = sessions
                    # log.duration += diff
                    log.save()
                    return AttendanceLogObj(id=log.id)
                else:
                    sessions = '[' + session + ']'
                    log = Log.objects.create(member=user, date=day, sessions=sessions)
                    return AttendanceLogObj(id=log.id)
            raise Exception('Wrong Password')
        raise Exception('User does not exist')

class Mutation(object):
    LogAttendance = LogAttendance.Field()