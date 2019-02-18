from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
from datetime import date

class Testimonial(models.Model):
    def get_dp_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/dp/' + filename

    message = models.TextField(null=True)
    author = models.CharField(null=True, max_length=100)
    credential = models.CharField(null=True, max_length=150)
    avatar = models.ImageField(default='',verbose_name='Profile Picture', upload_to=get_dp_path)

    class Meta:
        verbose_name_plural = "Testimonials"
        verbose_name = "Testimonial"

    def __str__(self):
        return self.author