import graphene
from framework.api.user import UserBasicObj
from django.db.models import F
from members.api.skill import SkillBasicObj
from members.api.social_project import SocialProjectObj
from ..models import Project, SocialProject


class ProjectBasicObj(graphene.ObjectType):
    name = graphene.String()
    slug = graphene.String()
    featured = graphene.Boolean()
    tagline = graphene.String()
    members = graphene.List(UserBasicObj)
    membersCount = graphene.Int()
    published = graphene.Date()
    cover = graphene.String()
    topics = graphene.List(SkillBasicObj)
    detail = graphene.String()
    links = graphene.List(SocialProjectObj)

    def resolve_membersCount(self, info):
        return Project.objects.annotate(
            username=F('members__username')
        ).filter(id=self['id']).count()

    @graphene.resolve_only_args
    def resolve_members(self):
        return Project.objects.values().annotate(
            username=F('members__username'),
            first_name=F('members__first_name'),
            last_name=F('members__last_name'),
            date_joined=F('members__date_joined'),
            is_active=F('members__is_active'),
            is_admin=F('members__is_superuser'),
        ).filter(id=self['id'])

    @graphene.resolve_only_args
    def resolve_topics(self):
        return Project.objects.values().annotate(
            name=F('topics__name'),
            type=F('topics__type'),
            icon=F('topics__icon')
        ).filter(id=self['id'])

    def resolve_links(self, info):
        return SocialProject.objects.values('link', 'portal').filter(project__id=self['id'])