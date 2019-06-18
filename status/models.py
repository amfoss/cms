from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import date


class Thread(models.Model):
    name = models.CharField(null=True,max_length=50)

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
