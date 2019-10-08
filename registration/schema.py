import graphene
from .models import *
from datetime import datetime
from graphql_jwt.decorators import permission_required, login_required
from django.db.models import Q
import ast
import json
import hashlib
from django.core.exceptions import ObjectDoesNotExist

from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, send_mail

from framework import settings

from_email = settings.EMAIL_HOST_USER


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
                    if form.applicationLimit is None or regCount < form.applicationLimit:
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
                            raise APIException('Registered already with the same email or phone number.',
                                               code='ALREADY_REGISTERED')
                    else:
                        raise APIException('Either Name or Phone Number is required.', code='REQUIRED_FIELD_MISSING')
                else:
                    raise APIException('Maximum possible applications already received for this form.',
                                       code='MAX_APPLICATIONS_EXCEDED')
            else:
                raise APIException('Submission deadline has passed', code='SUBMISSION_DEADLINE_ENDED')
        else:
            raise APIException('Applications are not accepted for this form right now.', code='INACTIVE_FORM')


class rsvpResponseObj(graphene.ObjectType):
    status = graphene.String()


class submitRSVP(graphene.Mutation):
    class Arguments:
        response = graphene.Boolean(required=True)
        hash = graphene.String(required=True)
        formID = graphene.Int(required=True)
        phone = graphene.String(required=True)
        formData = graphene.types.JSONString()

    Output = rsvpResponseObj

    def mutate(self, info, response, hash, formID, phone=None, formData=None):
        form = Form.objects.get(id=formID)
        if form:
            formHash = form.formHash
            application = Application.objects.get(phone=phone, form__id=formID)
            if application:
                hashStr = formHash + application.phone
                hashStrEncoded = hashlib.md5(hashStr.encode())
                hexHash = hashStrEncoded.hexdigest()
                if hash == hexHash:
                    application.rsvp = response
                    application.save()
                    return rsvpResponseObj(status='success')
                else:
                    raise APIException('Your token doesn\'t seem to be valid', code='INVALID_HASH')
            else:
                raise APIException('No application found with this phone number', code='INVALID_PHONE')
        else:
            raise APIException('This form is not found', code='INVALID_FORM')


class checkIn(graphene.Mutation):
    class Arguments:
        appID = graphene.Int(required=True)

    Output = rsvpResponseObj

    @login_required
    def mutate(self, info, appID):
        app = Application.objects.filter(id=appID).first()
        if app is not None:
            form = app.form
            if form.enableCheckIn:
                if app.checkIn:
                    raise APIException('The person has already checked-in.', code='ALREADY_CHECKED_IN')
                else:
                    app.checkIn = True
                    app.save()
                    return rsvpResponseObj(status='success')
            raise APIException('Check-In has not been enabled.', code='CHECK_IN_DISABLED')
        else:
            raise APIException('Person not found in the database', code='NOT_FOUND')


class Mutation(object):
    submitApplication = submitApplication.Field()
    submitRSVP = submitRSVP.Field()
    checkIn = checkIn.Field()


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
    id = graphene.Int()
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
    sendRSVPEmail = graphene.Field(rsvpResponseObj, applicationID=graphene.Int())
    getApplicant = graphene.Field(applicationObj, hash=graphene.String())

    def resolve_registrationForm(self, info, **kwargs):
        formID = kwargs.get('formID')
        return Form.objects.get(id=formID)

    @login_required
    def resolve_viewApplications(self, info, **kwargs):
        formID = kwargs.get('formID')
        return Application.objects.values().filter(form_id=formID)

    @login_required
    def resolve_sendRSVPEmail(self, info, **kwargs):
        applicationID = kwargs.get('applicationID')
        app = Application.objects.get(id=applicationID)
        form = app.form
        name = app.name
        email = app.email
        phone = app.phone
        formHash = form.formHash
        str = formHash + phone
        hashEncoded = hashlib.md5(str.encode())
        hash = hashEncoded.hexdigest()

        temp = Template(form.rsvpMessage)
        context = Context({'name': name, 'hash': hash})
        htmlMessage = temp.render(context)

        send_mail(
            form.rsvpSubject,
            strip_tags(htmlMessage),
            from_email,
            [email],
            html_message=htmlMessage,
            fail_silently=True,
        )

        return rsvpResponseObj(status="mails send")

    @login_required
    def resolve_getApplicant(self, info, **kwargs):
        hashCode = kwargs.get('hash')
        try:
            app = Application.objects.values().get(hash=hashCode)
        except ObjectDoesNotExist:
            raise APIException("Person not found in the database", code="NOT_FOUND")
        return app
