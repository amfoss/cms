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


class InviteUserGitLab(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            gitlab = GitLab(profile.gitlabUsername)
            gitlab.addUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class RemoveUserGitLab(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            gitlab = GitLab(profile.gitlabUsername)
            gitlab.removeUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class InviteUserGitHub(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            github = GitHub(profile.githubUsername)
            github.addUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class RemoveUserGitHub(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            github = GitHub(profile.githubUsername)
            github.removeUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class InviteUserCloudflare(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            cloudflare = Cloudflare(profile.email, profile.customEmail)
            cloudflare.addUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class RemoveUserCloudflare(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            cloudflare = Cloudflare(profile.email)
            cloudflare.removeUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class InviteUserTelegram(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            telegram = Telegram(profile.telegram_id)
            telegram.addUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class RemoveUserTelegram(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            telegram = Telegram(profile.telegram_id)
            telegram.removeUser()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class MakeUserInActive(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            gitlab = GitLab(profile.gitlabUsername)
            gitlab.removeUser()
            github = GitHub(profile.githubUsername)
            github.removeUser()
            cloudflare = Cloudflare(profile.email)
            cloudflare.removeUser()
            telegram = Telegram(profile.telegram_id)
            telegram.removeUser()
            user.is_active = False
            user.save()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class MakeUserActive(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = statusObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
            gitlab = GitLab(profile.gitlabUsername)
            gitlab.addUser()
            github = GitHub(profile.githubUsername)
            github.addUser()
            cloudflare = Cloudflare(profile.email, profile.customEmail)
            cloudflare.addUser()
            telegram = Telegram(profile.telegram_id)
            telegram.addUser()
            user.is_active = True
            user.save()
            return statusObj(status='Done')
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class Mutation(object):
    remove_user_gitlab = RemoveUserGitLab.Field()
    invite_user_gitlab = InviteUserGitLab.Field()
    remove_user_github = RemoveUserGitHub.Field()
    invite_user_github = InviteUserGitHub.Field()
    remove_user_cloudflare = RemoveUserCloudflare.Field()
    invite_user_cloudflare = InviteUserCloudflare.Field()
    remove_user_telegram = RemoveUserTelegram.Field()
    invite_user_telegram = InviteUserTelegram.Field()
    make_user_in_active = MakeUserInActive.Field()
    make_user_active = MakeUserActive.Field()
