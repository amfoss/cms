from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class StatusException(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='StatusException',
        verbose_name='User',
    )
    isPaused = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Status Update Exceptions"
        verbose_name = "Status Update Exception"

    def __str__(self):
        return self.user.username


class Thread(models.Model):
    name = models.CharField(max_length=200,  verbose_name="Name of Thread")
    isActive = models.BooleanField(verbose_name="Is Thread Active", default=True)
    enableGroupNotification = models.BooleanField(verbose_name="Should Send Report to Group?", default=True)
    allowBotToKick = models.BooleanField(verbose_name="Should bot kick members who didn't send updates?", default=True)
    noOfDays = models.IntegerField(verbose_name="Kick members after how many days ?", default=3, blank=True)
    email = models.EmailField(max_length=250, verbose_name="Thread Email")
    days = models.CharField(max_length=50, null=True, blank=True, verbose_name="Days # to be active, leave blank for all days")
    generationTime = models.CharField(max_length=50, verbose_name="Generation Time")
    dueTime = models.CharField(max_length=50, verbose_name="Due Time")
    logTime = models.CharField(max_length=50, verbose_name="Log Time")
    threadMessage = RichTextField(max_length=2000, verbose_name="Thread Email Message")
    footerMessage = models.CharField(max_length=500, verbose_name="Telegram Footer Message", null=True, blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    date = models.DateField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message = RichTextField(max_length=2500, verbose_name="Thread Body", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Messages"
        verbose_name = "Message"

    def __str__(self):
        return self.member.username


class DailyLog(models.Model):
    date = models.DateField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='threadMembers', blank=True)
    late = models.ManyToManyField(User, related_name='lateStatusLog', blank=True)
    didNotSend = models.ManyToManyField(User, related_name='didNotSendStatusLog', blank=True)

    class Meta:
        verbose_name_plural = "Daily Logs"
        verbose_name = "Daily Log"

    def __str__(self):
        return str(self.date) + ' - ' + self.thread.name
