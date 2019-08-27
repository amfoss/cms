from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Log(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Member", related_name='memberAttendance')
    date = models.DateField(verbose_name="Date", default=timezone.now)
    duration =  models.DurationField(verbose_name="Duration", null=True, blank=True)
    sessions = models.TextField(null=True, blank=True, verbose_name="Session JSON data")

    def __str__(self):
        return self.member.username