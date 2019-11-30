from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from members.models import Group


class Event(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100)

    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='EventCreator', blank=True, null=True)
    creationTime = models.DateTimeField(null=True, blank=True)
    lastEditor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='EventLastEditor', blank=True, null=True)
    lastEditTime = models.DateTimeField(null=True, blank=True)
    admins = models.ManyToManyField(User, related_name='EventAdmins', blank=True)
    sharedGroups = models.ManyToManyField(Group, blank=True)
    isPublic = models.BooleanField(default=False)

    startTimestamp = models.DateTimeField(verbose_name="Start Time")
    endTimestamp = models.DateTimeField(verbose_name="End Time", null=True, blank=True)
    isAllDay = models.BooleanField(default=False)
    details = RichTextField(max_length=5000, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.name
