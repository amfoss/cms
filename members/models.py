from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from status.models import Thread as StatusThread
from attendance.models import Module

import uuid
from datetime import date
from framework.validators import validate_file_size, processed_image_field_specs
from imagekit.models import ProcessedImageField

SKILL_TYPES = (('T', 'Technical'), ('A', 'Arts'), ('S', 'Social'), ('P', 'Sports'), ('O', 'Others'))
LEAVE_TYPE = (('M', 'Health'), ('F', 'Family/Home'), ('T', 'Tiredness'), ('A', 'Academics/Duty'))


class Skill(models.Model):
    def get_icon_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/icons/' + filename

    name = models.CharField(max_length=25)
    type = models.CharField(choices=SKILL_TYPES, default='O', max_length=1)
    icon = ProcessedImageField(
        default='./pages/static/pages/defaults/members-skill-icon-default.png',
        blank=True,
        verbose_name='Icon',
        upload_to=get_icon_path,
        null=True,
        validators=[validate_file_size],
        **processed_image_field_specs
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Portal(models.Model):
    name = models.CharField(max_length=25)
    icon = models.CharField(max_length=25, verbose_name='Icon Class', null=True)
    color = models.CharField(max_length=10, verbose_name='Color', help_text='hexcode with #', null=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    def get_icon_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/organizations/' + filename

    name = models.CharField(max_length=50)
    icon = ProcessedImageField(
        default='./pages/static/pages/defaults/members-organization-icon-default.jpg',
        blank=True,
        verbose_name='Logo/Icon',
        upload_to=get_icon_path,
        null=True,
        validators=[validate_file_size],
        **processed_image_field_specs
    )

    def __str__(self):
        return self.name


class Profile(models.Model):
    def get_dp_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/dp/' + filename

    def get_cover_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/cover/' + filename

    def get_resume_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/documents/resume/' + filename

    # Basic Info
    user = models.OneToOneField(
                User, on_delete=models.CASCADE,
                related_name='Profile',
                verbose_name='User',
    )
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=12, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    # Additional Details
    githubUsername = models.CharField(max_length=50, null=True, blank=True)
    telegram_id = models.CharField(max_length=50, null=True, blank=True)
    roll_number = models.CharField(max_length=25, null=True, blank=True)
    batch = models.IntegerField(null=True, help_text='Year of Admission', blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    birthday = models.DateField(null=True, help_text='YYYY-MM-DD', blank=True)
    tagline = models.CharField(max_length=80, null=True, blank=True)
    about = RichTextField(max_length=1000, null=True, blank=True)
    typing_speed = models.IntegerField(null=True, blank=True)
    resume = models.FileField(
                upload_to=get_resume_path,
                verbose_name='Attach Resume',
                null=True,
                blank=True,
                validators=[validate_file_size]
    )
    system_no = models.IntegerField(null=True, blank=True)
    cover = ProcessedImageField(
        default='',
        blank=True,
        verbose_name='Cover Picture',
        upload_to=get_cover_path,
        validators=[validate_file_size],
        **processed_image_field_specs,
        null=True,
    )
    accent = models.CharField(
            max_length=15,
            verbose_name='Accent Colour for Profile',
            help_text='Hex value with #',
            blank=True,
            null=True
    )

    # Relational Fields
    languages = models.ManyToManyField(Language, blank=True)
    interests = models.ManyToManyField(Skill, related_name='interests', blank=True)
    expertise = models.ManyToManyField(Skill, related_name='expertise', blank=True)
    experiences = models.ManyToManyField(Organization, related_name='WorkExperiences', through='WorkExperience')
    qualifications = models.ManyToManyField(
                Organization,
                related_name='EducationalQualifications',
                through='EducationalQualification'
    )
    links = models.ManyToManyField(Portal, related_name='SocialProfile', through='SocialProfile')

    class Meta:
        verbose_name_plural = "Profiles"
        verbose_name = "Profile"

    def __str__(self):
        return self.first_name


class SocialProfile(models.Model):
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, verbose_name='Portal Name')
    link = models.URLField(max_length=150,verbose_name='Profile URL')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Social Profile Links"
        verbose_name = "Social Profile Link"


class WorkExperience(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization', verbose_name='Organization')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    description = RichTextField(max_length=1000, null=True, blank=True)
    projects = models.ManyToManyField('activity.Project', blank=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Work Experiences"
        verbose_name = "Work Experience"


class EducationalQualification(models.Model):
    institution = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='institution', verbose_name='Institution')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = RichTextField(max_length=1000, null=True, blank=True)
    certificate = models.ManyToManyField('activity.Certificate', blank=True)
    projects = models.ManyToManyField('activity.Project', blank=True)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Educational Qualifications"
        verbose_name = "Educational Qualification"


class Responsibility(models.Model):
    title = models.CharField(max_length=100)
    about = RichTextField(max_length=2000, null=True, blank=True)
    thread = models.OneToOneField(StatusThread, on_delete=models.CASCADE, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='Responsibility', blank=True)

    class Meta:
        verbose_name_plural = "Responsibilities"
        verbose_name = "Responsibility"

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=100)

    admins = models.ManyToManyField(User, related_name='GroupAdmins')
    members = models.ManyToManyField(User, related_name='GroupMembers')

    attendanceEnabled = models.BooleanField(default=False, verbose_name="Attendance Enabled")
    attendanceModule = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Attendance Module")

    statusUpdateEnabled = models.BooleanField(default=False, verbose_name="Status Updates Enabled")
    thread = models.OneToOneField(StatusThread, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, verbose_name="Email to Send Thread")

    telegramBot = models.CharField(max_length=500, verbose_name="Telegram Bot Token")
    telegramGroup= models.CharField(max_length=250, verbose_name="Telegram Group ID")

    class Meta:
        verbose_name_plural = "Groups"
        verbose_name = "Group"

    def __str__(self):
        return self.name


class MentorGroup(models.Model):
    mentor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Mentor', verbose_name="Mentor Name")
    mentees = models.ManyToManyField(User, related_name="Mentees")

    sendReport = models.BooleanField(default=False, verbose_name="Send Reports")
    forwardStatusUpdates = models.BooleanField(default=False, verbose_name="Forward Status Updates")

    class Meta:
        verbose_name_plural = "Mentor Groups"
        verbose_name = "Mentor Group"

    def __str__(self):
        return self.mentor.username


class LeaveRecord(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='LeaveRecord')
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Approved By', related_name="LeaveApprover", null=True, blank=True)
    start_date = models.DateField(default=date.today, null=True, help_text='YYYY-MM-DD', verbose_name="From")
    end_date = models.DateField(default=date.today, null=True, help_text='YYYY-MM-DD', verbose_name="To", blank=True)
    type = models.CharField(choices=LEAVE_TYPE, default='T', max_length=2, verbose_name='Type')
    reason = models.TextField(null=True)

    class Meta:
        verbose_name_plural = "Leave Records"
        verbose_name = "Leave Record"

    def __str__(self):
        return self.member.username

__all__ = [
            'LeaveRecord',
            'MentorGroup',
            'Group',
            'Responsibility',
            'EducationalQualification',
            'WorkExperience',
            'SocialProfile',
            'Profile',
            'Language',
            'Skill',
            'Portal',
            'Organization'
]
