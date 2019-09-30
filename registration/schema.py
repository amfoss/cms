import graphene
from .models import *
from datetime import datetime
from graphql_jwt.decorators import permission_required, login_required
from django.db.models import Q
import ast
import json

class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['errorCode'] = code
        super().__init__(message)


class responseObj(graphene.ObjectType):
    id = graphene.String()
    status = graphene.String()


class submitApplication(graphene.Mutation):
    class Arguments:
        formID = graphene.Int(required=True)
        name = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        formData = graphene.types.JSONString()

    Output = responseObj

    def mutate(self, info, formID, name, email=None, phone=None, formData=None):
        form = Form.objects.get(id=formID)
        if form.isActive:
            if form.submissionDeadline is None or datetime.now() < form.submissionDeadline:
                regCount = Application.objects.filter(form_id=formID).count()
                if form.applicationLimit is None or regCount < form.applicationLimit or form.onSubmitAfterMax == 'W':
                    status = 'W'
                    if form.applicationLimit is None or regCount < form.applicationLimit :
                        status = 'U'
                    if email is not None or phone is not None:
                        apps = Application.objects.filter((Q(email=email) & Q(phone=phone)) & Q(form_id=formID))
                        apps.count()
                        if form.allowMultiple or apps.count() == 0:
                            app = Application.objects.create(
                                name=name,
                                submissionTime=datetime.now(),
                                form_id=formID,
                                email=email,
                                phone=phone,
                                formData=formData,
                                status=status
                            )
                            app.save()
                            return responseObj(id=app.id, status=status)
                        else:
                            raise APIException('Registered already with the same email or phone number.', code='ALREADY_REGISTERED')
                    else:
                        raise APIException('Either Name or Phone Number is required.', code='REQUIRED_FIELD_MISSING')
                else:
                    raise APIException('Maximum possible applications already received for this form.', code='MAX_APPLICATIONS_EXCEDED')
            else:
                raise APIException('Submission deadline has passed', code='SUBMISSION_DEADLINE_ENDED')
        else:
            raise APIException('Applications are not accepted for this form right now.', code='INACTIVE_FORM')


class Mutation(object):
    submitApplication = submitApplication.Field()


class formDetailsObj(graphene.ObjectType):
    name = graphene.String()
    allowMultiple = graphene.Boolean()
    applicationsCount = graphene.Int()

    def resolve_applicationsCount(self, info):
        return Application.objects.filter(form_id=self.id).count()


class formDataObj(graphene.ObjectType):
    key = graphene.String()
    value = graphene.String()

    def resolve_key(self, info):
        return self[0]

    def resolve_value(self, info):
        return self[1]


class applicationObj(graphene.ObjectType):
    name = graphene.String()
    submissionTime = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    formData = graphene.List(formDataObj)

    def resolve_formData(self, info):
        list = []
        if self['formData'] is not None:
            obj = ast.literal_eval(self['formData'])
            form = Form.objects.values().get(id=self['form_id'])
            fields = json.loads(form["formFields"])
            for field in fields:
                if field["key"] in obj:
                    list.append([field["key"], obj[field["key"]]])
                else:
                    list.append([field["key"], None])
            return list
        else:
            return None


class applicationsListObj(graphene.ObjectType):
    applicationCount = graphene.Int()
    applications = graphene.List(applicationObj)

    def resolve_applicationCount(self, info):
        return len(self)

    def resolve_applications(self, info):
        return self


class Query(object):
    registrationForm = graphene.Field(formDetailsObj, formID=graphene.Int())
    viewApplications = graphene.Field(applicationsListObj, formID=graphene.Int())

    def resolve_registrationForm(self, info, **kwargs):
        formID = kwargs.get('formID')
        return Form.objects.get(id=formID)

    @login_required
    def resolve_viewApplications(self, info, **kwargs):
        formID = kwargs.get('formID')
        return Application.objects.values().filter(form_id=formID)
