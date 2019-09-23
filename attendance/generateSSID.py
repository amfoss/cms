from .models import *
from datetime import date, datetime, timedelta
from django.utils import timezone

from .generatorScript import generatorScript

to_tz = timezone.get_default_timezone()
now = datetime.now().astimezone(to_tz)

def refreshSSID(thread):
    lastTime = thread.lastRefreshTime.astimezone(to_tz)
    if now - lastTime >= thread.seedRefreshInterval:
        seed = thread.seed
        newSeed = generatorScript(seed)
        thread.SSID = 'amFOSS_' + str(newSeed)
        thread.seed = newSeed
        thread.lastRefreshTime = now.replace(second=0, microsecond=0)
        thread.save()

