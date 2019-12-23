from django.db import models
from django.contrib.auth.models import User


class Password(models.Model):
    name = models.CharField(max_length=25)
    login_name = models.CharField(max_length=40)
    password = models.CharField(max_length=25)
    details = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    admins = models.ManyToManyField(User, related_name='admins')
    key = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Passwords"
        verbose_name = "Password"

    def __str__(self):
        return self.name
