import graphene
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User
from framework.api.user import UserBasicObj
from forms.models import *


class FormObj(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    creator = graphene.Field(UserBasicObj)
    creationTime = graphene.types.datetime.DateTime()
    lastEditor = graphene.Field(UserBasicObj)
    lastEditTime = graphene.types.datetime.DateTime()
    isActive = graphene.Boolean()
    allowMultiple = graphene.Boolean()
    submissionDeadline = graphene.types.datetime.DateTime()
    admissionLimit = graphene.Int()
    hasSlots = graphene.Boolean()
    entriesCount = graphene.Int()

    def resolve_hasSlots(self, info):
        obj = Form.objects.get(id=self['id'])
        if obj.slots.count() > 0:
            return True
        return False

    def resolve_entriesCount(self, info):
        return Entry.objects.filter(form=self['id']).count()

class Query(object):
    viewForms = graphene.List(FormObj)

    @login_required
    def resolve_viewForms(self, info, **kwargs):
        user = info.context.user
        if user.is_superuser:
            return Form.objects.values().all().order_by('-id')
        else:
            return Form.objects.values().filter(admins=user).order_by('-id')

