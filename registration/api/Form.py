import graphene
import json
from graphql_jwt.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from framework.api.user import UserBasicObj
from framework.api.APIException import APIException
from registration.models import *


class FormFieldObj(graphene.ObjectType):
    question = graphene.String()
    key = graphene.String()
    type = graphene.String()
    regex = graphene.String()
    required = graphene.Boolean()
    important = graphene.Boolean()


class FormObj(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    admins = graphene.List(UserBasicObj)
    isActive = graphene.Boolean()
    allowMultiple = graphene.Boolean()
    submissionDeadline = graphene.types.datetime.DateTime()
    admissionLimit = graphene.Int()
    entriesCount = graphene.Int()
    fields = graphene.List(FormFieldObj)

    def resolve_creator(self, info):
        try:
            user = User.objects.values().get(id=self['creator_id'])
        except ObjectDoesNotExist:
            user = None
        return user

    def resolve_lastEditor(self, info):
        try:
            user = User.objects.values().get(id=self['lastEditor_id'])
        except ObjectDoesNotExist:
            user = None
        return user

    def resolve_admins(self, info):
        try:
            users = Form.objects.get(id=self['id']).admins.all().values()
        except ObjectDoesNotExist:
            users = None
        return users

    def resolve_entriesCount(self, info):
        return Application.objects.filter(form=self['id']).count()

    def resolve_fields(self, info):
        return json.loads(self['formFields'])


class Query(object):
    viewForms = graphene.List(FormObj)
    getForm = graphene.Field(FormObj, formID=graphene.Int())
    getFormFields = graphene.List(FormFieldObj, formID=graphene.Int())

    @login_required
    def resolve_viewForms(self, info, **kwargs):
        user = info.context.user
        if user.is_superuser:
            return Form.objects.values().all().order_by('-id')
        else:
            return Form.objects.values().filter(admins=user).order_by('-id')

    @login_required
    def resolve_getForm(self, info, **kwargs):
        user = info.context.user
        formID = kwargs.get('formID')
        try:
            form = Form.objects.values().get(id=formID)
        except ObjectDoesNotExist:
            raise APIException('No form exists with the ID provided', code='FORM_NOT_FOUND')
        if user.is_superuser or user in Form.objects.get(id=formID).admins.all() or form.creator == user:
            return form
        else:
            raise APIException('You don\'t have permission to view this form', code='PERMISSION_DENIED')

    @staticmethod
    def resolve_getFormFields(self, info, **kwargs):
        formID = kwargs.get('formID')
        try:
            form = Form.objects.get(id=formID)
        except ObjectDoesNotExist:
            raise APIException('No form exists with the ID provided', code='FORM_NOT_FOUND')
        return json.loads(form.formFields)