from django.core.management.base import BaseCommand
import hashlib

from framework import settings
from ...models import Application, Form

from_email = settings.EMAIL_HOST_USER


class Command(BaseCommand):
    help = 'Exports & Sends Registration form applications to an email as a CSV'

    def add_arguments(self, parser):
        parser.add_argument('formID', type=int)

    def handle(self, *args, **options):
        formID = options['formID']
        apps = Application.objects.filter(form_id=formID)
        form = Form.objects.get(id=formID)
        formHash = form.formHash
        for app in apps:
            str = formHash + app.phone
            hashEncoded = hashlib.md5(str.encode())
            hash = hashEncoded.hexdigest()
            app.hash = hash
            app.save()

