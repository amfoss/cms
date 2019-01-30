from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Tag(models.Model):
    name = models.CharField(null=True, max_length=25)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(null=True,max_length=25)
    slug = models.SlugField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Parent')

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(null=True,max_length=50)
    slug =  models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Post', verbose_name='Author')
    content = RichTextField()
    featured_image = models.ImageField(default='', verbose_name='Featured Image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', blank=True)
    tags = models.ManyToManyField(Tag,verbose_name='Tag', blank=True)

    class Meta:
        verbose_name_plural = "Posts"
        verbose_name = "Post"

    def __str__(self):
        return self.title


class ExternalPost(models.Model):
    title = models.CharField(null=True,max_length=50)
    slug =  models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ExternalPost', verbose_name='Author')
    featured_image = models.ImageField(default='', verbose_name='Featured Image')
    url = models.URLField(max_length=100, verbose_name='Blog Post URL')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Tag', blank=True)

    class Meta:
        verbose_name_plural = "External Posts"
        verbose_name = "External Post"

    def __str__(self):
        return self.title

__all__ = ['ExternalPost','Tag','Category','Post']