# Generated by Django 2.1.7 on 2019-02-19 16:08

import activity.models
import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('attachment', models.FileField(blank=True, null=True, upload_to=activity.models.Certificate.get_certificate_path, verbose_name='Attach Certificate')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': 'Certificates',
                'verbose_name': 'Certificate',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': 'Courses',
                'verbose_name': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('C', 'Conference/Summit'), ('H', 'Hackathon'), ('D', 'Developer Meet'), ('I', 'Internship'), ('E', 'Student Exchange'), ('S', 'Summer School'), ('O', 'Others')], default='C', max_length=1)),
                ('date', models.DateField(default=datetime.date.today)),
                ('international', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'verbose_name_plural': 'Events',
                'verbose_name': 'Event',
            },
        ),
        migrations.CreateModel(
            name='Honour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Honours',
                'verbose_name': 'Honour',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField()),
                ('featured', models.BooleanField(default=False)),
                ('tagline', models.CharField(max_length=100, null=True)),
                ('published', models.DateField(default=datetime.date.today)),
                ('cover', models.ImageField(default='', upload_to=activity.models.Project.get_poster_path, verbose_name='Project Poster')),
                ('detail', ckeditor.fields.RichTextField(max_length=10000, null=True, verbose_name='Details')),
            ],
            options={
                'verbose_name_plural': 'Projects',
                'verbose_name': 'Project',
            },
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(max_length=100, verbose_name='Project Page URL')),
            ],
            options={
                'verbose_name_plural': 'Project Profile Links',
                'verbose_name': 'Project Profile Link',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Publications',
                'verbose_name': 'Publication',
            },
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='activity.Event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Talk', to=settings.AUTH_USER_MODEL, verbose_name='Member')),
            ],
            options={
                'verbose_name_plural': 'Talks',
                'verbose_name': 'Talk',
            },
        ),
    ]
