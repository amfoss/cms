import graphene
from hashlib import md5
from ..models import Profile, SocialProfile, Portal
from graphql_jwt.decorators import login_required


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
    username = graphene.String()
    tagline = graphene.String()
    about = graphene.String()
    gravatar = graphene.String()
    links = graphene.List(SocialProfileObj)
    githubUsername = graphene.String()
    # fields that require login
    profile_pic = graphene.String()
    phone = graphene.String()
    birthDay = graphene.types.datetime.Date()
    telegramID = graphene.String()
    roll = graphene.String()
    batch = graphene.Int()

    def resolve_firstName(self, info):
        return self['first_name']

    def resolve_lastName(self, info):
        return self['last_name']

    def resolve_fullName(self, info):
        if self['last_name'] is not None:
            return f"{self['first_name']} {self['last_name']}"
        else:
            return self['first_name']

    def resolve_username(self, info):
        return self['user__username']

    def resolve_gravatar(self, info):
        return "https://www.gravatar.com/avatar/" + md5(self['email'].lower().encode()).hexdigest()

    def resolve_links(self, info):
        return SocialProfile.objects.values('link', 'portal').filter(profile__id=self['id'])

    def resolve_githubUsername(self, info):
        return self['githubUsername']

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

    @login_required
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
