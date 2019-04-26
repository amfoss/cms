import uuid
from django.db import models
from ckeditor.fields import RichTextField
from datetime import date, datetime
from gallery.validators import validate_file_size, processed_image_field_specs
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import User

DIFFICULTY = (('1', 'Easy'), ('2', 'Moderate'), ('3', 'Tough'), ('4', 'Hard'))
TYPE = (('T', 'Technical'), ('N', 'Non-Technical'), ('R', 'Responsibility'), ('O', 'Other'))
TASK_STATUS = (('0', 'Assigned'), ('1', 'Started'), ('2', 'Submitted for Review'), ('3', 'Redo'), ('4', 'Verified'))


class Stream(models.Model):
    def get_icon_path(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/blog/cover/' + filename

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    type = models.CharField(choices=TYPE, default='t', max_length=1)
    description = RichTextField(max_length=2000, null=True, blank=True)
    icon = ProcessedImageField(
        verbose_name='Icon Image',
        upload_to=get_icon_path,
        validators=[validate_file_size],
        **processed_image_field_specs
    )
    color = models.CharField(max_length=10, verbose_name='Color', help_text='hexcode with #', null=True)
    parents = models.ManyToManyField('self', verbose_name='Parents', blank=True)

    class Meta:
        verbose_name_plural = "Streams"
        verbose_name = "Stream"

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = RichTextField(max_length=2000, null=True, blank=True)
    points = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 11)], default='2')
    difficulty = models.CharField(choices=DIFFICULTY, default='1', max_length=1)
    date = models.DateField(default=date.today)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Task', verbose_name='Author')
    stream = models.ManyToManyField(Stream, verbose_name='Stream', blank=True)

    class Meta:
        verbose_name_plural = "Tasks"
        verbose_name = "Task"

    def __str__(self):
        return self.title


class TaskLog(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='TaskLog', verbose_name='Member')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='Log', verbose_name='Task')
    status = models.CharField(choices=TASK_STATUS, default='1', verbose_name='Task Status', max_length=1)
    proof = RichTextField(max_length=2000, null=True, blank=True)
    reviewers = models.ManyToManyField(User, related_name='Reviewers', verbose_name='Task Reviewers', blank=True)
    start_time = models.DateTimeField(default=datetime.today)
    completion_time = models.DateTimeField(default=None, blank=True, null=True)
    points = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 10)], default='2')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_assigner', verbose_name='Task Assigner', null=True, blank=True)
    assign_time = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Task Logs"
        verbose_name = "Task Log"

    def __str__(self):
        return self.member + ' - ' + self.task.id
