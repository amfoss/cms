import graphene
from .models import *
from datetime import datetime
from django.db.models import Q
from graphql_jwt.decorators import permission_required, login_required
import json
import ast
from django.utils import timezone

to_tz = timezone.get_default_timezone()


class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['errorCode'] = code
        super().__init__(message)


class ResponseObj(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    slot = graphene.String()
    submissionTime = graphene.String()


class SubmitForm(graphene.Mutation):
    class Arguments:
        formID = graphene.Int(required=True)
        name = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        slot = graphene.Int()
        formData = graphene.types.JSONString()

    Output = ResponseObj

    def mutate(self, info, formID, name, email=None, phone=None, formData=None, slot=None):
        form = Form.objects.get(id=formID)
        if form.isActive:
            if form.submissionDeadline is None or datetime.now() < form.submissionDeadline:
                if email is not None or phone is not None:
                    apps = Entry.objects.filter((Q(email=email) | Q(phone=phone)) & Q(form_id=formID))
                    if form.allowMultiple or apps.count() == 0:
                        app = Entry.objects.create(
                            name=name,
                            submissionTime=datetime.now(),
                            form_id=formID,
                            email=email,
                            phone=phone,
                            formData=formData,
                            slot_id=slot
                        )
                        app.save()
                        if slot is not None:
                            SObj = FormSlot.objects.get(id=slot).slot
                            return ResponseObj(id=app.id, name=name, submissionTime=str(datetime.now()), email=email, phone=phone, slot=SObj.name)
                        else:
                            return ResponseObj(id=app.id, name=name, submissionTime=str(datetime.now()), email=email, phone=phone, slot=None)
                    else:
                        raise APIException('Registered already with the same email or phone number.',
                                               code='ALREADY_REGISTERED')
                else:
                    raise APIException('Either Name or Phone Number is required.', code='REQUIRED_FIELD_MISSING')
            else:
                raise APIException('Submission deadline has passed', code='SUBMISSION_DEADLINE_ENDED')
        else:
            raise APIException('Applications are not accepted for this form right now.', code='INACTIVE_FORM')


class Mutation(object):
    submitForm = SubmitForm.Field()


class SlotData(graphene.ObjectType):
    name = graphene.String()
    id = graphene.Int()


class SlotFillObj(graphene.ObjectType):
    id = graphene.Int()
    total = graphene.Int()
    filled = graphene.Int()
    slot = graphene.Field(SlotData)

    def resolve_total(self, info):
        return self['admissionLimit']

    def resolve_filled(self, info):
        return Entry.objects.filter(slot_id=self['id'], form_id=self['form_id']).count()

    def resolve_slot(self, info):
        return Slot.objects.get(id=self['slot_id'])


class FormDetailsObj(graphene.ObjectType):
    slots = graphene.List(SlotFillObj)

    def resolve_slots(self, info):
        return Form.objects.get(id=self).formslot_set.values()


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
    slot = graphene.String()
    formData = graphene.List(FormDataObj)

    def resolve_submissionTime(self, info):
        return self['submissionTime'].astimezone(to_tz)

    def resolve_slot(self, info):
        if FormSlot.objects.filter(id=self['slot_id']).count() == 1:
            return FormSlot.objects.get(id=self['slot_id']).slot.name
        else:
            return str(self['slot_id'])

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
                            if obj[field["key"]] != -1:
                                name = FormSlot.objects.get(id=obj[field["key"]]).slot.name
                                list.append([field["key"], name])
                            else:
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


class FormObj(graphene.ObjectType):
    name = graphene.String()
    isActive = graphene.Boolean()
    allowMultiple = graphene.Boolean()
    submissionDeadline = graphene.types.datetime.DateTime()
    admissionLimit = graphene.Int()


class Query(object):
    viewSlotsStats = graphene.Field(FormDetailsObj, formID=graphene.Int())
    viewEntries = graphene.List(EntryObj, formID=graphene.Int())
    viewForms = graphene.List(FormObj)

    def resolve_viewSlotsStats(self, info, **kwargs):
        return kwargs.get('formID')

    @login_required
    def resolve_viewEntries(self, info, **kwargs):
        formID = kwargs.get('formID')
        user = info.context.user
        form = Form.objects.get(id=formID)
        if user in form.admins or user.is_superuser:
            return Entry.objects.values().filter(form_id=formID)
        else:
            raise APIException('You don\'t have permission required to view entries of this form', code='ACCESS_DENIED')

    @login_required
    def resolve_viewForms(self, info, **kwargs):
        user = info.context.user
        if user.is_superuser:
            return Form.objects.values().all()
        else:
            return Form.objects.values().filter(admins=user)
