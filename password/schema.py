import graphene
from graphql_jwt.decorators import login_required

from .models import *
from framework.api.user import UserBasicObj
from django.db.models import F


class PasswordObj(graphene.ObjectType):
    name = graphene.String()
    loginName = graphene.String()
    password = graphene.String()
    details = graphene.String()
    admins = graphene.List(UserBasicObj)
    url = graphene.String()

    def resolve_name(self, info):
        return self['name']

    def resolve_loginName(self, info):
        return self['login_name']

    def resolve_password(self, info):
        return self['password']

    def resolve_details(self, info):
        return self['details']

    def resolve_admins(self, info):
        return Password.objects.annotate(
            username=F('admins__username'),
            first_name=F('admins__first_name'),
            last_name=F('admins__last_name'),
            date_joined=F('admins__date_joined'),
            is_active=F('admins__is_active'),
            is_admin=F('admins__is_superuser'),
        ).filter(id=self['id'])

    def resolve_url(self, info):
        return self['url']


class Query(object):
    viewAccounts = graphene.List(PasswordObj)

    @login_required
    def resolve_viewAccounts(self, info):
        user = info.context.user
        if user.is_superuser:
            return Password.objects.values().all().order_by('-id')
        else:
            return Password.objects.values().filter(admins=user).order_by('-id')
