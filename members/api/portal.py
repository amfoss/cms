import graphene


class PortalBasicObj(graphene.ObjectType):
    name = graphene.String()
    color = graphene.String()
    icon = graphene.String()

    def resolve_name(self, info):
        return self['name']

    def resolve_color(self, info):
        return self['color']

    def resolve_icon(self, info):
        return self['icon']
