import graphene
from graphql_jwt.decorators import login_required

from framework.api.APIException import APIException
from .models import *
from framework.api.user import UserBasicObj
from django.db.models import F


class PasswordLoginObj(graphene.ObjectType):
    name = graphene.String()
    url = graphene.String()

    def resolve_name(self, info):
        return self['name']

    def resolve_url(self, info):
        return self['url']


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
    viewAccounts = graphene.List(PasswordLoginObj)
    viewAccount = graphene.Field(PasswordObj, name=graphene.String(required=True), key=graphene.String(required=True))

    @login_required
    def resolve_viewAccounts(self, info):
        user = info.context.user
        if user.is_superuser:
            return Password.objects.values().all().order_by('-id')
        else:
            return Password.objects.values().filter(admins=user).order_by('-id')

    @login_required
    def resolve_viewAccount(self, info, **kwargs):
        name = kwargs.get('name')
        key = kwargs.get('key')
        password = Password.objects.get(name=name)
        user = info.context.user
        if user in password.admins.all() or user.is_superuser:
            if key == password.key:
                return Password.objects.values().get(name=name)
            else:
                raise APIException('Please enter the valid key',
                                   code='WRONG_KEY')
        else:
            raise APIException('Only Admins have access',
                               code='ONLY_ADMINS_HAS_ACCESS')
