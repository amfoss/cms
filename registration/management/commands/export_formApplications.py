import csv
import ast
import json
from django.core.management.base import BaseCommand
from io import StringIO
from django.core.mail import EmailMessage

from framework import settings
from ...models import Application, Form

from_email = settings.EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'Exports & Sends Registration form applications to an email as a CSV'

    def add_arguments(self, parser):
        parser.add_argument('formID', type=int)
        parser.add_argument('email', type=str)

    def handle(self, *args, **options):
        email = options['email']
        formID = options['formID']
        apps = Application.objects.filter(form_id=formID)
        fieldList = ['id', 'name', 'submissionTime', 'email', 'phone', 'rsvp', 'checkIn']
        form = Form.objects.values().get(id=formID)
        formFields = json.loads(form["formFields"])
        for field in formFields:
            fieldList.append(field["key"])
        appData = [fieldList]
        for app in apps:
            logRow = [app.id, app.name, app.submissionTime, app.email, app.phone, app.rsvp, app.checkIn]
            if app.formData is not None:
                formData = ast.literal_eval(app.formData)
            else:
                formData = ''
            for field in formFields:
                if formData != '' and field["key"] in app.formData:
                    logRow.append(formData[field["key"]])
                else:
                    logRow.append('')
            appData.append(logRow)

        csvfile = StringIO()
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(appData)

        email = EmailMessage(
            "Form Registrations",
            'Please find the attachment.',
            from_email,
            [email],
        )
        email.attach('formApplications.csv', csvfile.getvalue(), 'text/csv')
        email.send()

