import graphene
from members.api.profile import AvatarObj
from members.models import Profile


class UserBasicObj(graphene.ObjectType):
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    email = graphene.String()
    avatar = graphene.Field(AvatarObj)
    isMembershipActive = graphene.Boolean()
    isAdmin = graphene.Boolean()
    joinDateTime = graphene.types.datetime.DateTime()

    def resolve_firstName(self, info):
        return self['first_name']

    def resolve_lastName(self, info):
        return self['last_name']

    def resolve_fullName(self, info):
        return self['first_name'] + " " + self['last_name']

    def resolve_joinDateTime(self, info):
        return self['date_joined']

    def resolve_isMembershipActive(self, info):
        return self['is_active']

    def resolve_isAdmin(self, info):
        return self['is_superuser']

    def resolve_avatar(self, info):
        return Profile.objects.values().get(user__username=self['username'])