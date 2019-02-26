from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import date

class Thread(models.Model):
    name = models.CharField(null=True,max_length=50)

    def __str__(self):
        return self.name

class TaskTag(models.Model):
    name = models.CharField(null=True, max_length=50)
    colour = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

class TaskStatus(models.Model):
    name = models.CharField(null=True, max_length=50)

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

class Task(models.Model):
    title = models.CharField(null=True,max_length=50)
    description = RichTextField(max_length=300, null=True)
    assignees = models.ManyToManyField(User)
    due_date = models.DateField(default=date.today)
    team = models.ManyToManyField('members.Team', blank=True)
    tags = models.ManyToManyField(TaskTag, blank=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.SET_NULL, null=True)
    updates = models.ManyToManyField(Status, blank=True)

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"

    def __str__(self):
        return self.name

class StatusRegister(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.BooleanField(default=False)

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