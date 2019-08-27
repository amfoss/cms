from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date
from .validators import validate_file_size, processed_image_field_specs
from imagekit.models import ProcessedImageField

class Photo(models.Model) :
    def get_gallery_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/gallery/' + filename

    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    image = ProcessedImageField(default='', verbose_name='Image', upload_to=get_gallery_path,validators=[validate_file_size], **processed_image_field_specs)
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id) + str(self.uploader.username) + str(self.date)

    class Meta:
        verbose_name_plural = "Photos"
        verbose_name = "Photo"


class Album(models.Model) :
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    description = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    cover = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, related_name='featured_image')
    photos = models.ManyToManyField(Photo, related_name='album')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Albums"
        verbose_name = "Album"
