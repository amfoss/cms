from django.db import models


class Form(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)
    allowMultiple = models.BooleanField(default=False)
    submissionDeadline = models.DateTimeField(null=True, blank=True)
    applicationLimit = models.IntegerField(null=True, blank=True)
    formFields = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Forms"
        verbose_name = "Form"

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    submissionTime = models.DateTimeField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    formData = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Applications"
        verbose_name = "Application"

    def __str__(self):
        return self.name
