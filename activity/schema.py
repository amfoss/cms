import graphene
from graphene_django.types import DjangoObjectType
from .models import *

class ProjectObj(DjangoObjectType):
    class Meta:
        model = Project
        exclude_fields = ('id')

class ProjectLinkObj(DjangoObjectType):
    class Meta:
        model = ProjectLink
        exclude_fields = ('id','project')

class CertificateObj(DjangoObjectType):
    class Meta:
        model = Certificate
        exclude_fields = ('id')

class CourseObj(DjangoObjectType):
    class Meta:
        model = Course
        exclude_fields = ('id')

class HonourObj(DjangoObjectType):
    class Meta:
        model = Honour
        exclude_fields = ('id')

class TalkObj(DjangoObjectType):
    class Meta:
        model = Talk
        exclude_fields = ('id')

class Query(object):
    pass