from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import date

class Thread(models.Model):
    name = models.CharField(max_length=200,  verbose_name="Name of Thread")
    isActive = models.BooleanField(verbose_name="Whether the thread is Active?")
    sendReport = models.BooleanField(verbose_name="Should Send Report to Group?")
    threadEmail = models.EmailField(max_length=254, verbose_name="Email to Send Thread")
    telegramGroupID = models.CharField(max_length=200, verbose_name="Telegram Group ID")
    days = models.CharField(max_length=50, null=True, blank=True, verbose_name="Days # to be active, leave blank for all days")
    generationTime = models.CharField(max_length=50, verbose_name="Generation Time")
    dueTime = models.CharField(max_length=50, verbose_name="Due Time")
    logTime = models.CharField(max_length=50, verbose_name="Log Time")
    threadMessage = RichTextField(max_length=2000, verbose_name="Thread Message")

    def __str__(self):
        return self.name


class Log(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Logs"
        verbose_name = "Log"

    def __str__(self):
        return self.member.username
