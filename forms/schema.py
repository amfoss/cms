import graphene
from .models import *
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from framework.api.APIException import APIException

from forms.api.Form import Query as FormQueries
from forms.api.viewEntries import Query as viewEntries

to_tz = timezone.get_default_timezone()


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
                            return ResponseObj(id=app.id, name=name, submissionTime=str(datetime.now()), email=email,
                                               phone=phone, slot=SObj.name)
                        else:
                            return ResponseObj(id=app.id, name=name, submissionTime=str(datetime.now()), email=email,
                                               phone=phone, slot=None)
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


class Query(FormQueries, viewEntries, object):
    viewSlotsStats = graphene.Field(FormDetailsObj, formID=graphene.Int())

    @staticmethod
    def resolve_viewSlotsStats(self, info, **kwargs):
        return kwargs.get('formID')
