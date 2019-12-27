import graphene
from .models import *
from django.contrib.auth.models import User
from datetime import date, datetime
from django.conf import settings

from .api.profile import Query as profileQuery
from .api.group import Query as groupQuery
from .api.webspace import Query as webspaceQuery
from graphql_jwt.decorators import login_required
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


class UploadFiles(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    Output = AtObj

    @login_required
    def mutate(self, info, name=None):
        user = info.context.user
        files = info.context.FILES['imageFile']
        ws = WebSpace.objects.create(name=name, user=user, file_name=files)
        ws.save()

        return AtObj(id=ws.id)


class Mutation(object):
    RecordLeaveToday = RecordLeaveToday.Field()
    UploadFiles = UploadFiles.Field()


#
#       Queries
#

class Query(profileQuery, groupQuery, webspaceQuery):
    pass

