from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid
from datetime import date
from gallery.validators import validate_file_size
from imagekit.models import ProcessedImageField

processed_image_field_specs = {
    'format': 'JPEG',
    'options': {'quality': 70}
}

POST_STATUS = [
    ('U', 'Unlisted'),
    ('D', 'Draft'),
    ('P', 'Published')
]

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Parent', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Post(models.Model):
    def get_featured_image_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/blog/cover/' + filename

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    status = models.CharField(choices=POST_STATUS, default='D', max_length=1)
    featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Post', verbose_name='Author')
    content = RichTextField()
    date = models.DateField(default=date.today)
    featured_image = ProcessedImageField(default='', verbose_name='Featured Image', upload_to=get_featured_image_path, validators=[validate_file_size], **processed_image_field_specs)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Category', null=True, blank=True)
    tags = models.ManyToManyField(Tag,verbose_name='Tag', blank=True)
    album = models.ForeignKey('gallery.Album', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Posts"
        verbose_name = "Post"

    def __str__(self):
        return self.title


class ExternalPost(models.Model):
    def get_featured_image_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/blog/cover/' + filename

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    date = models.DateField(default=date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ExternalPost', verbose_name='Author')
    featured_image = ProcessedImageField(default='', verbose_name='Featured Image', validators=[validate_file_size], **processed_image_field_specs)
    url = models.URLField(max_length=100, verbose_name='Blog Post URL')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Category', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tag', blank=True)

    class Meta:
        verbose_name_plural = "External Posts"
        verbose_name = "External Post"

    def __str__(self):
        return self.title


__all__ = ['ExternalPost', 'Tag', 'Category', 'Post']
