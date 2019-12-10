import graphene
from graphql_jwt.decorators import permission_required, login_required
from graphene_django_extras import DjangoObjectType
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from graphene_django.filter import DjangoFilterConnectionField
from datetime import date, datetime
from django.conf import settings

from .api.profile import Query as profileQuery
from .api.group import Query as groupQuery
from .api.webspace import Query as webspaceQuery

#
#       Mutations
#

class AtObj(graphene.ObjectType):
    id = graphene.String()

class RecordLeaveToday(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        type = graphene.String(required=True)
        reason = graphene.String(required=True)
        bot_token = graphene.String(required=True)
        token = graphene.String(required=True)

    Output = AtObj

    def mutate(self, info, user_id, type, reason, bot_token, token):
        profile = Profile.objects.get(telegram_id=user_id)
        user = User.objects.get(username=profile.user.username)
        d =date.today()
        if bot_token == settings.TELEGRAM_BOT_TOKEN:
            lr = LeaveRecord.objects.create(member=user, start_date=d, end_date=d, type=type, reason=reason)
            return AtObj(id=lr.id)
        raise Exception('Invalid bot token')


class Mutation(object):
    RecordLeaveToday = RecordLeaveToday.Field()


#
#       Queries
#

class Query(profileQuery, groupQuery, webspaceQuery):
    pass

