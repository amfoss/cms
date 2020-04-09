import graphene


class SkillBasicObj(graphene.ObjectType):
    name = graphene.String()
    type = graphene.String()
    icon = graphene.String()

    def resolve_name(self, info):
        return self['name']

    def resolve_type(self, info):
        return self['type']

    def resolve_icon(self, info):
        return self['icon']
