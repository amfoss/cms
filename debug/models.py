from django.db import models


class Errors(models.Model):
    module = models.CharField(verbose_name='module name', max_length=100)
    errorContent = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Errors"
        verbose_name = "Error"

    def __str__(self):
        return self.module
