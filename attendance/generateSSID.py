from .models import *
from datetime import date, datetime, timedelta
from django.utils import timezone

from .generatorScript import generatorScript

to_tz = timezone.get_default_timezone()
now = datetime.now().astimezone(to_tz)

def refreshSSID(module):
    lastTime = module.lastRefreshTime.astimezone(to_tz)
    if module.isPaused is False and now - lastTime >= module.seedRefreshInterval:
        seed = module.seed
        newSeed = generatorScript(seed)
        module.SSID = 'amFOSS_' + str(newSeed)
        module.seed = newSeed
        module.lastRefreshTime = now.replace(second=0, microsecond=0)
        module.save()

