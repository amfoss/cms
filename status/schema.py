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
    status = graphene.String(required=True)

class FetchDailyStatusUpdates(graphene.Mutation):
    class Arguments:
        date = graphene.types.datetime.Date(required=True)
        data = graphene.List(StatusInput)
        token = graphene.String(required=True)

    Output = StatusObj

    @permission_required('auth.delete_user')
    def mutate(self, info, data, date, token):
        name = 'Status Update Thread - ' + str(date.day) + '/' + str(date.month) + '/' + str(date.year)
        ids = list()
        t = Thread.objects.get_or_create(name=name)
        for e in data:
            user = User.objects.get(username=e.username)
            su = Status.objects.filter(author=user,thread=t[0]).all()
            if not su:
                s = Status.objects.create(author=user, thread=t[0], date=e.timestamp, status=e.status )
                ids.append(s.id)
        return StatusObj(ids=ids)

class Mutation(object):
    FetchDailyStatusUpdates = FetchDailyStatusUpdates.Field()

#
#       Queries
#