import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import *


class ProjectObj(DjangoObjectType):
    class Meta:
        model = Project
        exclude_fields = ('id')


class ProjectLinkObj(DjangoObjectType):
    class Meta:
        model = ProjectLink
        exclude_fields = ('id', 'project')


class CertificateObj(DjangoObjectType):
    class Meta:
        model = Certificate
        exclude_fields = ('id')


class CourseObj(DjangoObjectType):
    class Meta:
        model = Course
        exclude_fields = ('id')



class Query(object):
    projects = graphene.List(ProjectObj, username=graphene.String(required=False))

    def resolve_projects(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            user = User.objects.get(username=username)
            return Project.objects.filter(members=user)
        else:
            return Project.objects.all()
