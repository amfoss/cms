import telegram
from django.core.management.base import BaseCommand
from status.management.fetch_status_updates import DailyStatus
from datetime import date, datetime, timedelta
from members.models import Profile
from status.models import StatusRegister
from framework import settings
from pytz import timezone
from operator import itemgetter



class Command(BaseCommand):
    help = 'Logs Daily Status Updates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            help='Whether to test',
        )

    def handle(self, *args, **options):
        profiles = Profile.objects.all()

        members = dict()
        for profile in profiles:
            members[profile.id] = StatusRegister.objects.filter(member=profile.user).count()
        desc = dict(sorted(members.items(), key=itemgetter(1), reverse=True))
        asc = dict(sorted(members.items(), key=itemgetter(1)))

        message = '<b>Status Update Report</b> \n\n'

        message += '<b>Most Status Updates: </b>\n\n'
        i = 0
        last_val = -1
        for member in desc:
            if last_val > desc[member] or last_val < 0:
                i =  i+1
                if i>10:
                    break
                profile = Profile.objects.get(id=member)
                message +=  str(i) + ". " + str(profile.first_name)
                if profile.last_name:
                    message +=  ' ' + str(profile.last_name)
                message += " - " + str(desc[member]) + '\n'
                last_val = desc[member]

        message += '\n<b>Least Status Updates: </b>\n\n'
        i = 0
        last_val = -1
        for member in asc:
            if asc[member] > 0:
                if last_val < asc[member]:
                    i = i + 1
                    if i > 10:
                        break
                    profile = Profile.objects.get(id=member)
                    message += str(i) + ". " + str(profile.first_name)
                    if profile.last_name:
                        message += ' ' + str(profile.last_name)
                    message += " - " + str(asc[member]) + '\n'
                    last_val = asc[member]

        message += '\n<i>This is an automatically generated message. Please send your status updates daily.</i>'

        print(message)
        if not options['test']:
            # Send Message through Telegram Bot
            bot = telegram.Bot(
                token=settings.TELEGRAM_BOT_TOKEN)
            bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_ID,
                text=message,
                parse_mode=telegram.ParseMode.HTML
            )
