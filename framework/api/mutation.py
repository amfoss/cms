import graphene
from django.contrib.auth.models import User
from members.models import Profile, Group
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
        cmsGroup = graphene.Boolean()
        groupName = graphene.String()
        displayInWebsite = graphene.String()

    Output = statusObj

    def mutate(self, info, username, github=None, gitlab=None, telegram=None, cloudflare=None, cms=None, cmsGroup=None, groupName=None, displayInWebsite=None):
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
                user.is_active = cms
                user.save()

            if cmsGroup is not None and groupName is not None:
                if cmsGroup:
                    group = Group.objects.get(name=groupName)
                    group.members.add(user)
                    group.save()
                else:
                    group = Group.objects.get(name=groupName)
                    group.members.remove(user)
                    group.save()

            if displayInWebsite is not None:
                profile.displayInWebsite = displayInWebsite
                profile.save()

            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class AddToPlatform(graphene.Mutation):
    class Arguments:
        usernames = graphene.List(graphene.String)
        platform = graphene.String()

    Output = statusObj

    def mutate(self, info, usernames, platform):
        if info.context.user.is_superuser:
            for username in usernames:
                profile = Profile.objects.get(user__username=username)
                if platform is not None:
                    if platform == "gitlab":
                        GitLab(profile.gitlabUsername).addUser()
                    elif platform == "github":
                        GitHub(profile.githubUsername).addUser()
                    elif platform == "telegram":
                        Telegram(profile.telegram_id).addUser()
                else:
                    raise APIException('Platform is required to perform this action',
                                       code='PLATFORM_IS_REQUIRED')
            return statusObj(status=True)
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class Mutation(object):
    change_user_platform = ChangeUserPlatform.Field()
    addToPlatform = AddToPlatform.Field()