from django.db import models
from datetime import date
import uuid
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField
from framework.validators import validate_file_size, processed_image_field_specs


class Category(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Category_Author', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='Tag_Author', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


class News(models.Model):
    def get_poster_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/news/cover/' + filename

    title = models.CharField(max_length=100)
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='news_author', blank=True, null=True)
    pinned = models.BooleanField(default=False)
    cover = ProcessedImageField(default='', verbose_name='News Poster', upload_to=get_poster_path, validators=[validate_file_size], **processed_image_field_specs)
    date = models.DateField(default=date.today)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='category_author', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    description = RichTextField(null=True, blank=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title
