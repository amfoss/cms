from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Module(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name of Module")
    SSID = models.CharField(max_length=1000, verbose_name="Current WiFi SSID", default="amfoss_")
    seed = models.IntegerField(verbose_name="Current Seed", default=1000)
    seedRefreshInterval = models.DurationField(verbose_name="Seed Refresh Min")
    lastRefreshTime = models.DateTimeField(verbose_name="Last Seed Refresh Time", default=timezone.now)
    generationTime = models.CharField(max_length=50, verbose_name="Generation Time")
    logTime = models.CharField(max_length=50, verbose_name="Log Time")
    enableGroupNotification = models.BooleanField(verbose_name="Should Send Report to Group?", default=True)

    footerMessage = models.CharField(max_length=500, verbose_name="Telegram Footer Message", null=True, blank=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Member", related_name='memberAttendance')
    date = models.DateField(verbose_name="Date", default=timezone.now)
    duration = models.DurationField(verbose_name="Duration", null=True, blank=True)
    sessions = models.TextField(null=True, blank=True, verbose_name="Session JSON data")
    modules = models.ManyToManyField(Module)

    def __str__(self):
        return self.member.username
