import graphene
from members.models import Portal
from members.api.portal import PortalBasicObj


class SocialProjectObj(graphene.ObjectType):
    link = graphene.String()
    portal = graphene.Field(PortalBasicObj)

    def resolve_portal(self, info):
        return Portal.objects.values().get(id=self['portal'])