from django.db import models
import uuid
from gallery.validators import validate_file_size, processed_image_field_specs
from imagekit.models import ProcessedImageField

class Testimonial(models.Model):
    def get_dp_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/images/dp/' + filename

    message = models.TextField(null=True)
    author = models.CharField(null=True, max_length=100)
    credential = models.CharField(null=True, max_length=150)
    image = ProcessedImageField(default='', verbose_name='Profile Picture', upload_to=get_dp_path, validators=[validate_file_size], **processed_image_field_specs)

    class Meta:
        verbose_name_plural = "Testimonials"
        verbose_name = "Testimonial"

    def __str__(self):
        return self.author