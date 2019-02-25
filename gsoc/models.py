from django.db import models
from django.contrib.auth.models import User
from members.models import Skill, Organization
from gallery.validators import validate_file_size

GSoC_Status = (('C', 'Completed (3rd Evaluation)'), ('2','Second Evaluation'), ('1','First Evaluation'), ('S', 'Selected'), ('A', 'Applied'), ('T', 'Trying'), ('M','Mentored'))

class GSoC(models.Model):
    def get_proposal_link(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return 'static/uploads/documents/gsoc-proposals/' + filename

    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='GSoC', verbose_name='Member')
    organisation = models.ForeignKey(Organization, on_delete=models.SET_NULL, related_name='GSoCOrganisation', null=True)
    status = models.CharField(choices=GSoC_Status, default='T', max_length=1)
    year = models.IntegerField()
    proposal = models.FileField(upload_to=get_proposal_link, verbose_name='Attach Proposal',null=True,blank=True, validators=[validate_file_size])
    project = models.ForeignKey('activity.Project', related_name='GSoCProject', on_delete=models.SET_NULL, null=True, blank=True)
    link = models.URLField(max_length=150,verbose_name='External URL', blank=True, null=True)
    topics = models.ManyToManyField(Skill, related_name='GSoCTopics', blank=True)

    class Meta:
        verbose_name_plural = "GSoCs"
        verbose_name = "GSoC"

    def __str__(self):
        return self.member.username + ' - ' + self.organisation.name

