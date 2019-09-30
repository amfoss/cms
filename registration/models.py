from django.db import models

APPLICATION_STATUS = (('A', 'Accepted'), ('R', 'Rejected'), ('W', 'Waitlisted'), ('U', 'Under Review'))
ONFILL_OPTIONS = (('W', 'Waitlist'), ('D', 'Don\'t Accept'))


class Form(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name of the Form')
    isActive = models.BooleanField(default=True, verbose_name='Is Active?')
    allowMultiple = models.BooleanField(default=False, verbose_name='Allow Multiple?')
    submissionDeadline = models.DateTimeField(null=True, blank=True, verbose_name='Submission Deadline')
    applicationLimit = models.IntegerField(null=True, blank=True, verbose_name='Application Limit')
    formFields = models.TextField(blank=True, null=True, verbose_name='Form Fields')
    onSubmitAfterMax = models.CharField(choices=ONFILL_OPTIONS, max_length=1, blank=True, null=True, verbose_name='On Submit after limit?')

    class Meta:
        verbose_name_plural = "Forms"
        verbose_name = "Form"

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    submissionTime = models.DateTimeField()
    status = models.CharField(choices=APPLICATION_STATUS, default='U', max_length=1)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    formData = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Applications"
        verbose_name = "Application"

    def __str__(self):
        return self.name
