import graphene
from .models import *
from datetime import datetime
from django.db.models import Q


class applicationObj(graphene.ObjectType):
    id = graphene.String()


class submitApplication(graphene.Mutation):
    class Arguments:
        formID = graphene.Int(required=True)
        name = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        formData = graphene.types.JSONString()

    Output = applicationObj

    def mutate(self, info, formID, name, email=None, phone=None, formData=None):
        form = Form.objects.get(id=formID)
        if email is not None or phone is not None:
            apps = Application.objects.filter(Q(email=email) | Q(phone=phone) & Q(form_id=formID))
            if form.allowMultiple or apps.count() == 0:
                app = Application.objects.create(
                    name=name,
                    submissionTime=datetime.now(),
                    form_id=formID,
                    email=email,
                    phone=phone,
                    formData=formData
                )
                app.save()
                return applicationObj(id=app.id)
            else:
                raise Exception('Registered already with the same email or phone number.')
        else:
            raise Exception('Either Name or Phone Number is required.')


class Mutation(object):
    submitApplication = submitApplication.Field()


class formDetailsObj(graphene.ObjectType):
    name = graphene.String()
    allowMultiple = graphene.Boolean()
    applicationsCount = graphene.Int()

    def resolve_applicationsCount(self, info):
        return Application.objects.filter(form_id=self.id).count()


class Query(object):
    registrationForm = graphene.Field(formDetailsObj, formID=graphene.Int())

    def resolve_registrationForm(self, info, **kwargs):
        formID = kwargs.get('formID')
        return Form.objects.get(id=formID)
