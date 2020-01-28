from .models import *
from datetime import date, datetime, timedelta
from django.utils import timezone

import json

from .generatorScript import generatorScript
from .schema import update_futureSSID

to_tz = timezone.get_default_timezone()
now = datetime.now().astimezone(to_tz)


def refreshSSID(module):
    lastTime = module.lastRefreshTime.astimezone(to_tz)
    if module.isPaused is False and now - lastTime >= module.seedRefreshInterval:

        time = datetime.now() - timedelta(minutes=5)
        recentLogsCount = Log.objects.filter(lastSeen__gte=time).count()

        if recentLogsCount == 0:
            module.lastRefreshTime = now.replace(second=0, microsecond=0)
            return

        # open file and move list by 1 place

        seed = module.seed
        newSeed = generatorScript(seed)
        module.SSID = 'amFOSS_' + str(newSeed)
        module.seed = newSeed
        module.lastRefreshTime = now.replace(second=0, microsecond=0)
        with open("attendance/futureSSID.json", "r") as file:
            futureSSID = json.load(file)
        futureSSID = futureSSID[1:]
        update_futureSSID(futureSSID)
        module.save()
