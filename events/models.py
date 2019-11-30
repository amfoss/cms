from django.contrib.auth.models import User
from django.db import models
from forms.models import Form, Entry
from ckeditor.fields import RichTextField

APPLICATION_STATUS = (('A', 'Accepted'), ('R', 'Rejected'), ('W', 'WaitListed'), ('U', 'Under Review'))
ON_FILL_OPTIONS = (('W', 'WaitList'), ('D', 'Don\'t Accept'))


class Slot(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name/Title')

    def __str__(self):
        return str(self.id)


class Event(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name of the Event')
    registrationForm = models.ForeignKey(Form, on_delete=models.CASCADE)
    registrationLimit = models.IntegerField(null=True, blank=True, verbose_name='Application Limit')
    onSubmitAfterMax = models.CharField(choices=ON_FILL_OPTIONS,
                                        max_length=1,
                                        blank=True,
                                        null=True,
                                        verbose_name='On Submit after limit?'
                                        )
    rsvpSubject = models.TextField(blank=True, null=True)
    rsvpMessage = RichTextField(max_length=5000, verbose_name="RSVP Email Message")
    enableCheckIn = models.BooleanField(default=False, verbose_name="Enable Check-In")
    checkInSlots = models.ManyToManyField(Slot, related_name='EventCheckInSlots', through='CheckInSlot')
    eventHash = models.CharField(max_length=500, blank=True, null=True, verbose_name='Security hash for the Event')


class CheckInSlot(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, verbose_name='Slot')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='Event')
    startTime = models.DateTimeField(blank=True, null=True)
    endTime = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('slot', 'event',)


class Participant(models.Model):
    formEntry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(choices=APPLICATION_STATUS, default='U', max_length=1)
    hash = models.CharField(max_length=1000, blank=True, null=True)
    checkIn = models.ManyToManyField(CheckInSlot, related_name='ParticipantCheckIn', through='CheckIn')


class CheckIn(models.Model):
    slot = models.ForeignKey(CheckInSlot, on_delete=models.CASCADE, verbose_name='CheckIn Slot')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Participant')
    timestamp = models.DateTimeField(blank=True, null=True)
    verifier = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        unique_together = ('slot', 'participant',)
