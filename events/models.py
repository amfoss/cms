from django.db import models
from gallery.models import Album
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name='Title of the event')
    slug = models.CharField(max_length=50, blank=True, verbose_name='Slug')
    content = models.TextField(blank=True, null=True, verbose_name='Content')
    date = models.DateTimeField(verbose_name="Event Date", default=timezone.now)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True)
    creator = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Events', verbose_name='User', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.name
