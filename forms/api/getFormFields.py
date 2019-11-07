import graphene
import json
from forms.models import Form


class FormFieldsObj(graphene.ObjectType):
    name = graphene.String()
    key = graphene.String()
    required = graphene.String()
    isSlot = graphene.Boolean()
    isImportant = graphene.Boolean()


class Query(object):
    getFormFields = graphene.List(FormFieldsObj, formID=graphene.Int())

    @staticmethod
    def resolve_getFormFields(self, info, **kwargs):
        formID = kwargs.get('formID')
        return json.loads(Form.objects.get(id=formID).formFields)
