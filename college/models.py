from django.db import models
from django.contrib.auth.models import User

BRANCHES = (
    ('CSE', 'Computer Science & Engineering'),
    ('CAI', 'Computer Science (AI)'),
    ('ECE', 'Electronics & Communication Engineering'),
    ('EEE', 'Electrical & Electronics Engineering'),
    ('ME', 'Mechanical Engineering'),
    ('EIC', 'Electronics and Instrumentation Engineering'),
    ('ElectronicsCS', 'Electronics and Computer Engineering'),
    ('ElectricalCS', 'Electrical and Computer Engineering'),
    ('O', 'Others')
)


class Profile(models.Model):
    user = models.OneToOneField(
                User, on_delete=models.CASCADE,
                related_name='StudentProfile',
                verbose_name='User',
    )
    rollNo = models.CharField(verbose_name='rollNo', max_length=50, null=True, blank=True)
    admissionYear = models.IntegerField(verbose_name='Year of Admission')
    branch = models.CharField(choices=BRANCHES, default='CSE', max_length=35)
    classSection = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Student Profiles"
        verbose_name = "Student Profile"
