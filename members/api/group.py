import graphene
from framework.api.user import UserBasicObj
from ..models import Group
from django.db.models import F
from graphql_jwt.decorators import login_required


class GroupObj(graphene.ObjectType):
    name = graphene.String()
    statusUpdateEnabled = graphene.Boolean()
    attendanceEnabled = graphene.Boolean()
    admins = graphene.List(UserBasicObj)
    members = graphene.List(UserBasicObj)
    membersCount = graphene.Int()

    def resolve_membersCount(self, info):
        return len(self['members'])

    def resolve_admins(self, info):
        return Group.objects.annotate(
            username=F('admins__username'),
            first_name=F('admins__first_name'),
            last_name=F('admins__last_name'),
            date_joined=F('admins__date_joined'),
            is_active=F('admins__is_active'),
            is_admin=F('admins__is_superuser'),
        ).filter(id=self['id'])

    def resolve_members(self, info):
        return Group.objects.annotate(
            username=F('members__username'),
            first_name=F('members__first_name'),
            last_name=F('members__last_name'),
            date_joined=F('members__date_joined'),
            is_active=F('members__is_active'),
            is_admin=F('members__is_superuser'),
        ).filter(id=self['id'])


class Query(object):
    group = graphene.Field(
        GroupObj,
        id=graphene.Int(required=True)
    )
    groups = graphene.List(GroupObj)

    @login_required
    def resolve_group(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Group.objects.values().get(id=id)
        raise Exception('Group ID is a required parameter')

    @login_required
    def resolve_groups(self, info, **kwargs):
        return Group.objects.values().all()
