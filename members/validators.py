from django.core.exceptions import ValidationError
from imagekit.processors import ResizeToFit

def validate_file_size(value):
    if value:
        filesize = value.size

        if filesize > 10485761:
            raise ValidationError("The maximum file size that can be uploaded is 10MB.")
        else:
            return value

processed_image_field_specs = {
    'format': 'JPEG',
    'processors': [ResizeToFit(10000000, 2000)],
    'options': {'quality': 70}
}
