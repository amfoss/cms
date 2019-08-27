from django.db import models
from django.contrib.auth.models import User
from gallery.models import Album
from ckeditor.fields import RichTextField
from members.models import Skill, Portal, Organization
from datetime import date
import uuid
from gallery.validators import validate_file_size, processed_image_field_specs
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

class Project(models.Model):
    def get_poster_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/projects/' + filename

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
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

__all__ = ['Project', 'Portal', 'Course', 'Certificate', 'ProjectLink']
