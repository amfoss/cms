import graphene
from .models import *
from graphql_jwt.decorators import permission_required, login_required

#
#       Mutations
#


class StatusObj(graphene.ObjectType):
    ids = graphene.List(graphene.String)


class StatusInput(graphene.InputObjectType):
    timestamp = graphene.types.datetime.DateTime(required=True)
    username = graphene.String(required=True)
    status = graphene.Boolean(required=True)


class FetchDailyStatusUpdates(graphene.Mutation):
    class Arguments:
        data = graphene.List(StatusInput)
        token = graphene.String(required=True)

    Output = StatusObj

    @permission_required('auth.delete_user')
    def mutate(self, info, data, token):
        ids = list()
        for e in data:
            user = User.objects.get(username=e.username)
            s = StatusRegister.objects.create(member=user, timestamp=e.timestamp, status=True)
            ids.append(s.id)
        return StatusObj(ids=ids)


class Mutation(object):
    FetchDailyStatusUpdates = FetchDailyStatusUpdates.Field()

#
#       Queries
#