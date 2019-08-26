from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import date

class Thread(models.Model):
    name = models.CharField(max_length=100,  verbose_name="Name of Thread")
    isActive = models.BooleanField(verbose_name="Whether the thread is Active?")
    sendReport = models.BooleanField(verbose_name="Should Send Report to Group?")
    threadEmail = models.EmailField(max_length=254, verbose_name="Email to Send Thread")
    telegramGroupID = models.CharField(max_length=200, verbose_name="Telegram Group ID")
    days = models.CharField(max_length=50, null=True, blank=True, verbose_name="Days # to be active, leave blank for all days")
    generationTime = models.CharField(max_length=50, verbose_name="Generation Time")
    dueTime = models.CharField(max_length=50, verbose_name="Due Time")
    logTime = models.CharField(max_length=50, verbose_name="Log Time")
    threadMessage = RichTextField(max_length=1000, verbose_name="Thread Message")

    def __str__(self):
        return self.name


class Status(models.Model):
    date = models.DateTimeField(auto_now=True,verbose_name='Posted on')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, null=True, blank=True)
    status = RichTextField(max_length=300, null=True)

    class Meta:
        verbose_name_plural = "Status Updates"
        verbose_name = "Status Update"

    def __str__(self):
        if self.thread is not None:
            return self.thread.name + ' by @' + self.author.username
        else:
            return self.author.username


class StatusRegister(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Member Status Register"
        verbose_name = "Member Status Entry"

    def __str__(self):
        return self.member.username


class Notification(models.Model):
    title = models.CharField(null=True, max_length=50)
    groups = models.ManyToManyField('members.group')
    date = models.DateField(default=date.today)
    description = RichTextField(max_length=300, null=True)

    class Meta:
        verbose_name_plural = "Notifications"
        verbose_name = "Notification"

    def __str__(self):
        return self.title
