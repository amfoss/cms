import graphene
from ..models import Project
from members.api.project_basic import ProjectBasicObj


class Query(object):
    project = graphene.Field(
        ProjectBasicObj,
        slug=graphene.String(required=True)
    )
    projects = graphene.List(
        ProjectBasicObj,
        username=graphene.String()
    )

    def resolve_project(self, info, **kwargs):
        slug = kwargs.get('slug')
        if slug is not None:
            return Project.objects.values().get(slug=slug)
        raise Exception('Project Slug is a required parameter')

    def resolve_projects(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return Project.objects.values().filter(members__username=username)
        return Project.objects.values().all()
