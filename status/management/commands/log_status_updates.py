from django.core.management.base import BaseCommand
from status.management.fetch_status_updates import DailyStatus
from datetime import date
from members.models import Profile
from status.models import StatusRegister


class Command(BaseCommand):
    help = 'Updates Status Update Register'

    def handle(self, *args, **options):
        d = date(2019, 4, 1)
        log = DailyStatus(d)
        profiles = Profile.objects.filter(email__in=log.emails)
        print(log.emails)
        for profile in profiles:
            if profile.user.is_active:
                StatusRegister.objects.create(member=profile.user, timestamp=log.members[profile.email], status=True)

