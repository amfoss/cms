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


class UploadFileObj(graphene.ObjectType):
    fileName = graphene.String()


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


class UpdateProfilePic(graphene.Mutation):
    Output = UploadFileObj

    @login_required
    def mutate(self, info):
        user = info.context.user
        profilePic = info.context.FILES['imageFile']
        profile = Profile.objects.get(user=user)
        profile.profile_pic = profilePic
        profile.save()

        return UploadFileObj(fileName=profile.profile_pic)


class UploadFiles(graphene.Mutation):
    Output = UploadFileObj

    @login_required
    def mutate(self, info):
        user = info.context.user
        files = info.context.FILES['imageFile']
        ws = WebSpace.objects.create(user=user, file_name=files)
        ws.save()

        return UploadFileObj(fileName=ws.file_name)


class Mutation(object):
    RecordLeaveToday = RecordLeaveToday.Field()
    UploadFiles = UploadFiles.Field()
    UpdateProfilePic = UpdateProfilePic.Field()


#
#       Queries
#

class Query(profileQuery, groupQuery, webspaceQuery):
    pass

