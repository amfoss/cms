from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

APPLICATION_STATUS = (('A', 'Accepted'), ('R', 'Rejected'), ('W', 'Waitlisted'), ('U', 'Under Review'))
ONFILL_OPTIONS = (('W', 'Waitlist'), ('D', 'Don\'t Accept'))


def get_first_user():
    return User.objects.first()


class Form(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name of the Form')
    isActive = models.BooleanField(default=True, verbose_name='Is Active?')
    allowMultiple = models.BooleanField(default=False, verbose_name='Allow Multiple?')
    submissionDeadline = models.DateTimeField(null=True, blank=True, verbose_name='Submission Deadline')
    applicationLimit = models.IntegerField(null=True, blank=True, verbose_name='Application Limit')
    formFields = models.TextField(blank=True, null=True, verbose_name='Form Fields')
    onSubmitAfterMax = models.CharField(choices=ONFILL_OPTIONS, max_length=1, blank=True, null=True, verbose_name='On Submit after limit?')
    formHash = models.CharField(max_length=500, blank=True, null=True, verbose_name='Security hash for the form')
    rsvpSubject = models.TextField(blank=True, null=True)
    rsvpMessage = RichTextField(max_length=5000, verbose_name="RSVP Email Message")
    enableCheckIn = models.BooleanField(default=False, verbose_name="Enable Check-In")
    admins = models.ManyToManyField(User, related_name='formAdmins', blank=True, default=get_first_user)

    class Meta:
        verbose_name_plural = "Forms"
        verbose_name = "Form"

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100)
    hash = models.CharField(max_length=1000, blank=True, null=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    submissionTime = models.DateTimeField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    formData = models.TextField(blank=True, null=True)
    status = models.CharField(choices=APPLICATION_STATUS, default='U', max_length=1)
    rsvp = models.BooleanField(blank=True, null=True)
    checkIn = models.BooleanField(blank=True, null=True)
    checkInTime = models.DateTimeField(blank=True, null=True)
    checkedInBy = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    details = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Applications"
        verbose_name = "Application"

    def __str__(self):
        return self.name
