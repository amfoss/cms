import graphene
from django.contrib.auth.models import User
from members.models import Profile
from .APIException import APIException

from framework.platforms.gitlab import GitLab
from framework.platforms.github import GitHub
from framework.platforms.cloudflare import Cloudflare
from framework.platforms.telegram import Telegram


class statusObj(graphene.ObjectType):
    status = graphene.String()


class ChangeUserPlatform(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        github = graphene.Boolean()
        gitlab = graphene.Boolean()
        telegram = graphene.Boolean()
        cloudflare = graphene.Boolean()
        cms = graphene.Boolean()

    Output = statusObj

    def mutate(self, info, username, github=None, gitlab=None, telegram=None, cloudflare=None, cms=None):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            if gitlab is not None:
                if gitlab:
                    GitLab(profile.gitlabUsername).addUser()
                else:
                    GitLab(profile.gitlabUsername).removeUser()

            if github is not None:
                if github:
                    GitHub(profile.githubUsername).addUser()
                else:
                    GitHub(profile.githubUsername).removeUser()

            if telegram is not None:
                if telegram:
                    Telegram(profile.telegram_id).addUser()
                else:
                    Telegram(profile.telegram_id).removeUser()

            if cloudflare is not None:
                if cloudflare:
                    Cloudflare(profile.email, profile.customEmail).addUser()
                else:
                    Cloudflare(profile.email, profile.customEmail).removeUser()

            if cms is not None:
                if cms:
                    user.is_active = True
                else:
                    user.is_active = False

            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class Mutation(object):
    change_user_platform = ChangeUserPlatform.Field()
