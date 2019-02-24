from django.db import models
from django.contrib.auth.models import User
from gallery.models import Album
from ckeditor.fields import RichTextField
from members.models import Skill, Portal, Organization
from datetime import date
import uuid
from gallery.validators import validate_file_size,
from imagekit.models import ProcessedImageField

EVENT_TYPES = [
    ('C', 'Conference/Summit'),
    ('H', 'Hackathon'),
    ('D', 'Developer Meet'),
    ('I', 'Internship'),
    ('E', 'Student Exchange'),
    ('S', 'Summer School'),
    ('O', 'Others')
]

processed_image_field_specs = {
    'format': 'JPEG',
    'options': {'quality': 70}
}

class Project(models.Model):
    def get_poster_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/projects/' + filename

    name = models.CharField(max_length=200)
    slug = models.SlugField()
    featured = models.BooleanField(default=False)
    tagline = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='Project')
    published = models.DateField(default=date.today)
    cover = ProcessedImageField(default='', verbose_name='Project Poster', upload_to=get_poster_path, validators=[validate_file_size], **processed_image_field_specs)
    topics = models.ManyToManyField(Skill, related_name='ProjectTopics', blank=True)
    detail = RichTextField(verbose_name='Details')
    links = models.ManyToManyField(Portal, related_name='ProjectLinks', through='ProjectLink')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Projects"
        verbose_name = "Project"

    def __str__(self):
        return self.name


class ProjectLink(models.Model):
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE, related_name='project_links_portal',
                               verbose_name='Portal Name')
    link = models.URLField(max_length=100, verbose_name='Project Page URL')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Project Profile Links"
        verbose_name = "Project Profile Link"


class Certificate(models.Model):
    def get_certificate_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/documents/certificates/' + filename

    title = models.CharField(max_length=200)
    attachment = models.FileField(upload_to=get_certificate_path, verbose_name='Attach Certificate',null=True,blank=True, validators=[validate_file_size])
    member = models.ForeignKey(User,on_delete=models.CASCADE, related_name='Certificate', verbose_name='Certified')
    topics = models.ManyToManyField(Skill, related_name='CertificateTopics', blank=True)
    date = models.DateField(default=date.today)
    issuer = models.ForeignKey(Organization, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Certificates"
        verbose_name = "Certificate"

    def __str__(self):
        return self.title


class Course(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(null=True, blank=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Course', verbose_name='Member')
    topics = models.ManyToManyField(Skill, related_name='CourseTopics', blank=True)
    date = models.DateField(default=date.today)
    issuer = models.ForeignKey(Organization, on_delete=models.PROTECT)
    certificate = models.ForeignKey(Certificate, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Courses"
        verbose_name = "Course"

    def __str__(self):
        return self.name


class Honour(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.ForeignKey(Organization, on_delete=models.PROTECT)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Honour', verbose_name='Member')
    date = models.DateField(default=date.today)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    certificate = models.ForeignKey(Certificate, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    topics = models.ManyToManyField(Skill, related_name='HonourTopic', blank=True)

    class Meta:
        verbose_name_plural = "Honours"
        verbose_name = "Honour"

    def __str__(self):
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=200)
    publisher = models.ForeignKey(Organization, on_delete=models.PROTECT)
    members = models.ManyToManyField(User, related_name='Publication', verbose_name='Member')
    date = models.DateField(default=date.today)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    topics = models.ManyToManyField(Skill, related_name='PublicationTopic', blank=True)

    class Meta:
        verbose_name_plural = "Publications"
        verbose_name = "Publication"

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(choices=EVENT_TYPES, default='C', max_length=1)
    attendee = models.ManyToManyField(User, related_name='EventAttendee', blank=True)
    date = models.DateField(default=date.today)
    international = models.BooleanField(default=False, blank=True, null=True)
    topics = models.ManyToManyField(Skill, related_name='EventTopics', blank=True)
    projects = models.ManyToManyField(Project, related_name='EventProject', blank=True)
    honours = models.ManyToManyField(Honour, related_name='EventHonours', blank=True)
    organizer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Events"
        verbose_name = "Event"

    def __str__(self):
        return self.title


class Talk(models.Model):
    title = models.CharField(max_length=200)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Talk', verbose_name='Member')
    date = models.DateField(default=date.today)
    topics = models.ManyToManyField(Skill, related_name='TalkTopics', blank=True)
    organizer = models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Talks"
        verbose_name = "Talk"

    def __str__(self):
        return self.title


__all__ = ['Event', 'Talk', 'Project', 'Portal', 'Course', 'Certificate', 'Publication', 'ProjectLink', 'Honour']
