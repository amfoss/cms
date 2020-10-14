from django.db import models
from registration.models import Form
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Emails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=True, null=True)
    category = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Emails"
        verbose_name = "Email"

    def __str__(self):
        return self.name


class Mailer(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, null=True)
    generationEmailDate = models.DateField(default=None, verbose_name="Date")
    generationEmailTime = models.CharField(max_length=20, verbose_name="Time")
    subject = models.CharField(max_length=50, verbose_name="Email Message subject")
    threadMessage = RichTextField(max_length=2000, verbose_name="Email Message")

    class Meta:
        verbose_name_plural = "Mailer"
        verbose_name = "Mailer"

    def __str__(self):
        return self.name


class Token(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='TokenCreator', blank=True, null=True)
    creationTime = models.DateTimeField(null=True, blank=True)
    lastEditor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='TokenLastEditor', blank=True, null=True)
    lastEditTime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Tokens"
        verbose_name = "Token"

    def __str__(self):
        return self.key
