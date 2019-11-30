from django.db import models
from django.contrib.auth.models import User


class Slot(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name/Title')

    def __str__(self):
        return self.name


class Form(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name of the Form')

    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='FormCreator', blank=True, null=True)
    creationTime = models.DateTimeField(null=True, blank=True)
    lastEditor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='FormLastEditor', blank=True, null=True)
    lastEditTime = models.DateTimeField(null=True, blank=True)
    admins = models.ManyToManyField(User, related_name='FormAdmins', blank=True)

    isActive = models.BooleanField(default=True, verbose_name='Is Active?')
    allowMultiple = models.BooleanField(default=False, verbose_name='Allow Multiple?')
    submissionDeadline = models.DateTimeField(null=True, blank=True, verbose_name='Submission Deadline')
    admissionLimit = models.IntegerField(null=True, blank=True, verbose_name='Admission Limit')
    slots = models.ManyToManyField(Slot, through='FormSlot', related_name='FormSlots')
    formFields = models.TextField(blank=True, null=True, verbose_name='Form Fields')

    class Meta:
        verbose_name_plural = "Forms"
        verbose_name = "Form"

    def __str__(self):
        return self.name


class FormSlot(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, verbose_name='slot')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name='Form')
    admissionLimit = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Form Slot"
        verbose_name = "Form Slot"
        unique_together = ('slot', 'form',)

    def __str__(self):
        return self.slot.name + ' - ' + self.form.name


class Entry(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    formData = models.TextField(blank=True, null=True)
    slot = models.ForeignKey(FormSlot, on_delete=models.PROTECT, null=True, blank=True)

    submissionTime = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Entries"
        verbose_name = "Entry"

    def __str__(self):
        return self.name
