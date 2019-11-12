import json
from django.core.management.base import BaseCommand

from members.models import Group
from status.logger import log


class Command(BaseCommand):
    help = 'Imports Messages from MessageData.json file'

    def handle(self, *args, **options):
        thread_id = 3
        f = open("MessageData.json", 'r')
        data = json.loads(f.read())
        data.reverse()
        members = []
        groups = Group.objects.filter(thread_id=thread_id, statusUpdateEnabled=True)
        for group in groups:
            for member in group.members.all():
                members.append(member)
        log(data, members, thread_id)
