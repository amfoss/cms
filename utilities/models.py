from django.db import models
from registration.models import Form
from ckeditor.fields import RichTextField


class Mailer(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    generationEmailDate = models.DateField(default=None, verbose_name="Date")
    generationEmailTime = models.CharField(max_length=20, verbose_name="Time")
    subject = models.CharField(max_length=50, verbose_name="Email Message subject")
    threadMessage = RichTextField(max_length=2000, verbose_name="Email Message")

    class Meta:
        verbose_name_plural = "Mailer"
        verbose_name = "Mailer"

    def __str__(self):
        return self.name
