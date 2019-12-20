import graphene
import json
import ast
from django.utils import timezone
from graphql_jwt.decorators import login_required

from registration.models import Application, Form
from framework.api.APIException import APIException

to_tz = timezone.get_default_timezone()


class FormDataObj(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()

    def resolve_key(self, info):
        return self[0]

    def resolve_value(self, info):
        return self[1]


class EntryObj(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    submissionTime = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    formData = graphene.List(FormDataObj)
    details = graphene.String()

    def resolve_submissionTime(self, info):
        return self['submissionTime'].astimezone(to_tz)

    def resolve_formData(self, info):
        list = []
        if self['formData'] is not None:
            obj = ast.literal_eval(self['formData'])
            form = Form.objects.values().get(id=self['form_id'])
            fields = json.loads(form["formFields"])
            for field in fields:
                if field["key"] in obj:
                    if "isSlot" in field.keys():
                        if field["isSlot"]:
                            list.append([field["key"], None])
                        else:
                            list.append([field["key"], obj[field["key"]]])
                    else:
                        list.append([field["key"], obj[field["key"]]])
                else:
                    list.append([field["key"], None])
            return list
        else:
            return None


class Query(object):
    viewEntries = graphene.List(EntryObj, formID=graphene.Int())

    @login_required
    def resolve_viewEntries(self, info, **kwargs):
        formID = kwargs.get('formID')
        user = info.context.user
        form = Form.objects.get(id=formID)
        if user in form.admins.all() or user.is_superuser:
            return Application.objects.values().filter(form_id=formID)
        else:
            raise APIException('You don\'t have permission required to view entries of this form', code='ACCESS_DENIED')