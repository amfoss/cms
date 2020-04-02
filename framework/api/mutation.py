import graphene
from django.contrib.auth.models import User
from members.models import Profile
from .APIException import APIException

from framework.platforms.gitlab import GitLab
from framework.platforms.github import GitHub


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
    make_user_in_active = MakeUserInActive.Field()
    make_user_active = MakeUserActive.Field()