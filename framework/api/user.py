import graphene
from members.api.profile import AvatarObj
from members.models import Profile
from members.api.profile import ProfileObj
from status.models import Message
from activity.models import *
from django.db.models import F


class CategoryBasicObj(graphene.ObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self['name']

    def resolve_author(self, info):
        return User.objects.values().get(id=self['author_id'])


class TagBasicObj(graphene.ObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self['name']


class BlogBasicObj(graphene.ObjectType):
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    date = graphene.Date(required=True)
    tags = graphene.List(TagBasicObj)
    draft = graphene.String(required=True)
    featured = graphene.Boolean()
    description = graphene.String(required=True)
    cover = graphene.String(required=True)
    category = graphene.Field(CategoryBasicObj)

    def resolve_title(self, info):
        return self['title']

    def resolve_slug(self, info):
        return self['slug']

    def resolve_author(self, info):
        return User.objects.values().get(id=self['author_id'])

    def resolve_date(self, info):
        return self['date']

    @graphene.resolve_only_args
    def resolve_tags(self):
        return Blog.objects.values().annotate(
            name=F('tags__name'),
        ).filter(id=self['id'])

    def resolve_draft(self, info):
        return self['draft']

    def resolve_featured(self, info):
        return self['featured']

    def resolve_description(self, info):
        return self['description']

    def resolve_cover(self, info):
        return self['cover']

    def resolve_category(self, info):
        return Category.objects.values().get(id=self['category_id'])


class AchievementBasicObj(graphene.ObjectType):
    title = graphene.String(required=True)
    year = graphene.Int(required=True)
    description = graphene.String(required=True)
    category = graphene.Field(CategoryBasicObj)

    def resolve_title(self, info):
        return self['title']

    def resolve_year(self, info):
        return self['year']

    def resolve_description(self, info):
        return self['description']

    def resolve_category(self, info):
        return Category.objects.values().get(id=self['category_id'])


class UserBasicObj(graphene.ObjectType):
    username = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    avatar = graphene.Field(AvatarObj)
    isMembershipActive = graphene.Boolean()
    isAdmin = graphene.Boolean()
    joinDateTime = graphene.types.datetime.DateTime()
    statusUpdateCount = graphene.Int()
    lastStatusUpdate = graphene.Date()
    admissionYear = graphene.Int()
    profile = graphene.Field(ProfileObj)
    blogs = graphene.List(BlogBasicObj)
    achievements = graphene.List(AchievementBasicObj)

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

    def resolve_statusUpdateCount(self, info):
        return Message.objects.values().filter(member__username=self['username']).count()

    def resolve_lastStatusUpdate(self, info):
        return Message.objects.values().filter(member__username=self['username']).order_by('-date').first()['date']

    def resolve_admissionYear(self, info):
        return Profile.objects.values().get(user__username=self['username'])['batch']

    def resolve_profile(self, info):
        return Profile.objects.values().get(user__username=self['username'])

    def resolve_blogs(self, info):
        return Blog.objects.values().filter(author__username=self['username'])

    def resolve_achievements(self, info):
        return Achievements.objects.values().filter(user__username=self['username'])
