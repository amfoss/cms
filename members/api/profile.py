import graphene
from hashlib import md5
from ..models import Profile, SocialProfile, Portal
from graphql_jwt.decorators import login_required
from framework import settings
from framework.api.APIException import APIException

from github import Github
import gitlab
import CloudFlare
import telegram

GITLAB_TOKEN = settings.GITLAB_TOKEN
GITHUB_TOKEN = settings.GITHUB_TOKEN
EMAIL_USER = settings.EMAIL_HOST_USER
CLOUDFLARE_TOKEN = settings.CLOUDFLARE_TOKEN
CLOUDFLARE_ZONE_ID = settings.CLOUDFLARE_ZONE_ID
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID


class PortalObj(graphene.ObjectType):
    name = graphene.String()
    color = graphene.String()
    icon = graphene.String()


class SocialProfileObj(graphene.ObjectType):
    link = graphene.String()
    portal = graphene.Field(PortalObj)

    def resolve_portal(self, info):
        return Portal.objects.values().get(id=self['portal'])


class ProfileObj(graphene.ObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    tagline = graphene.String()
    about = graphene.String()
    gravatar = graphene.String()
    links = graphene.List(SocialProfileObj)
    githubUsername = graphene.String()
    gitlabUsername = graphene.String()
    customEmail = graphene.String()
    # fields that require login
    inGitLabGroup = graphene.Boolean()
    inGitHubGroup = graphene.Boolean()
    inCloudFlareGroup = graphene.Boolean()
    inTelegramGroup = graphene.Boolean()
    profilePic = graphene.String()
    phone = graphene.String()
    birthDay = graphene.types.datetime.Date()
    telegramID = graphene.String()
    roll = graphene.String()
    batch = graphene.String()

    def resolve_firstName(self, info):
        return self['first_name']

    def resolve_lastName(self, info):
        return self['last_name']

    def resolve_fullName(self, info):
        if self['last_name'] is not None:
            return f"{self['first_name']} {self['last_name']}"
        else:
            return self['first_name']

    def resolve_gravatar(self, info):
        return "https://www.gravatar.com/avatar/" + md5(self['email'].lower().encode()).hexdigest()

    def resolve_links(self, info):
        return SocialProfile.objects.values('link', 'portal').filter(profile__id=self['id'])

    def resolve_githubUsername(self, info):
        return self['githubUsername']

    def resolve_gitlabUsername(self, info):
        return self['gitlabUsername']

    def resolve_customEmail(self, info):
        return self['customEmail']

    def resolve_profilePic(self, info):
        return self['profile_pic']

    @login_required
    def resolve_inGitLabGroup(self, info):
        if info.context.user.is_superuser:
            if self['gitlabUsername']:
                gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
                gl.auth()
                group = gl.groups.get('amfoss')
                userID = gl.users.list(username=self['gitlabUsername'])[0].id
                try:
                    member = group.members.get(userID)
                    if member:
                        return True
                except:
                    return False
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inGitHubGroup(self, info):
        if info.context.user.is_superuser:
            if self['githubUsername']:
                g = Github(GITHUB_TOKEN)
                ghuser = g.get_user(self['githubUsername'])
                org = g.get_organization('amfoss')
                if org.has_in_members(ghuser):
                    return True
                else:
                    return False
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inCloudFlareGroup(self, info):
        if info.context.user.is_superuser:
            if self['email']:
                cf = CloudFlare.CloudFlare(email=EMAIL_USER, token=CLOUDFLARE_TOKEN)
                records = cf.zones.dns_records.get(CLOUDFLARE_ZONE_ID, params={'per_page': 50})
                for record in records:
                    if record['type'] == 'TXT' and record['name'] == 'amfoss.in' and record['content'].startswith(
                            'forward-email'):
                        if self['email'] in record['content']:
                            return True
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inTelegramGroup(self, info):
        if info.context.user.is_superuser:
            bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
            try:
                status = bot.get_chat_member(chat_id=TELEGRAM_CHAT_ID, user_id=self['telegram_id']).status
                if status == "left" or status == "kicked":
                    return False
                else:
                    return True
            except:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_birthDay(self, info):
        return self['birthday']

    @login_required
    def resolve_phone(self, info):
        return self['phone']

    @login_required
    def resolve_telegramID(self, info):
        return self['telegram_id']

    @login_required
    def resolve_roll(self, info):
        return self['roll_number']

    def resolve_batch(self, info):
        return self['batch']


class AvatarObj(graphene.ObjectType):
    githubUsername = graphene.String()

    def resolve_githubUsername(self, info):
        return self['githubUsername']


class Query(object):
    profile = graphene.Field(
        ProfileObj,
        username=graphene.String(required=True)
    )
    profiles = graphene.List(ProfileObj)
    getAvatar = graphene.Field(AvatarObj, username=graphene.String(required=True))

    def resolve_profile(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return Profile.objects.values().get(user__username=username)
        raise Exception('Username is a required parameter')

    def resolve_profiles(self, info, **kwargs):
        return Profile.objects.values().all()

    def resolve_getAvatar(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return Profile.objects.values().get(user__username=username)
        raise Exception('Username is a required parameter')
