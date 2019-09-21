import graphene
from graphene_django_extras import DjangoObjectType
from status.models import Log
from django.contrib.auth.models import User


class StatusObj(DjangoObjectType):
    class Meta:
        model = Log
        exclude_fields = ('id',)


class Query(object):
    getStatusUpdates = graphene.List(StatusObj, date=graphene.types.datetime.DateTime(required=True))
    getMembersStatusUpdates = graphene.List(StatusObj, username=graphene.String(required=True))

    def resolve_getStatusUpdates(self, **kwargs):
        date = kwargs.get('date')
        return Log.objects.filter(timestamp=date)

    def resolve_getMemberStatusUpdates(self, **kwargs):
        username = kwargs.get('username')
        user = User.objects.get(username=username)
        return Log.objects.filter(member=user)
