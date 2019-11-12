import dateutil.parser
from django.contrib.auth.models import User
from status.models import Thread, Message, DailyLog
from pytz import timezone
from django.core.exceptions import ObjectDoesNotExist


def log(data, members, thread_id):
    thread = Thread.objects.get(id=thread_id)

    for entry in data:
        try:
            user = User.objects.get(email=entry['email'])
            timestamp = dateutil.parser.parse(entry['timestamp'])
            logDate = dateutil.parser.parse(entry['date']).date()

            msgObj, msgCreated = Message.objects.get_or_create(
                member=user,
                date=logDate,
                timestamp=timestamp,
                thread=thread,
                message=entry['message']
            )
            msgObj.save()
            if msgCreated:
                obj, created = DailyLog.objects.get_or_create(
                    date=logDate,
                    thread=thread,
                )
                if created:
                    obj.members.add(*members)
                    obj.didNotSend.add(*members)

                if user in obj.members.all():
                    dueTime = timezone("Asia/Calcutta").localize(
                        dateutil.parser.parse(entry['date']).replace(hour=int(thread.dueTime[:2]),
                                                                     minute=int(thread.dueTime[2:])))

                    if user in obj.didNotSend.all():
                        if timestamp > dueTime:
                            obj.late.add(user)
                        obj.didNotSend.remove(user)
                obj.save()

        except ObjectDoesNotExist:
            pass
