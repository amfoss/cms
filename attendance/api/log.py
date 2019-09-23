import graphene
from graphql_jwt.decorators import login_required
from ..models import Log
from django.db.models import F
from datetime import date, datetime, timedelta
from django.utils import timezone
from framework.api.user import UserBasicObj
from django.contrib.auth.models import User


class liveMembersObj(graphene.ObjectType):
    count = graphene.Int()
    members = graphene.List(UserBasicObj)

    def resolve_count(self, info):
        return len(self)

    def resolve_members(self, info):
        return User.objects.filter(username__in=self)


class Query(object):
    liveMembers = graphene.Field(liveMembersObj)

    @login_required
    def resolve_liveMembers(self, info):
        time = datetime.now() - timedelta(minutes=5)
        logs = Log.objects.annotate(
            username=F('member__username')
        ).filter(lastSeen__gte=time).values('username')
        u = []
        for i in logs:
            u.append(i['username'])
        return u
