import graphene
import graphql_jwt
from datetime import date, datetime, timedelta

from django.contrib.auth.hashers import check_password
from django.utils import timezone
from graphql_jwt.decorators import permission_required, login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

import attendance.schema
from college.schema import Query as collegeQuery
from dairy.schema import Query as dairyQuery
from registration.schema import Mutation as registrationMutation, Query as registrationQuery
import activity.schema
import tasks.schema
import status.schema
import password.schema
from .api.APIException import APIException
from college.api.profile import StudentProfileObj
from college.models import Profile as CollegeProfile
from dairy.schema import Mutation as eventMutation

from members.schema import Query as MembersQuery, Mutation as membersMutation
from members.api.profile import ProfileObj
from members.api.group import GroupObj
from members.models import Profile, Group

from attendance.models import Log
from attendance.api.log import userAttendanceObj

from .api.user import UserBasicObj

to_tz = timezone.get_default_timezone()


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password',)


class UserObj(UserBasicObj, graphene.ObjectType):
    profile = graphene.Field(ProfileObj)
    groups = graphene.List(GroupObj)
    attendance = graphene.Field(
        userAttendanceObj,
        startDate=graphene.types.datetime.Date(),
        endDate=graphene.types.datetime.Date()
    )
    isInLab = graphene.Boolean()
    lastSeenInLab = graphene.types.datetime.DateTime()
    collegeProfile = graphene.Field(StudentProfileObj)

    def resolve_profile(self, info):
        return Profile.objects.values().get(user__username=self['username'])

    def resolve_collegeProfile(self, info):
        return CollegeProfile.objects.values().get(user__username=self['username'])

    @login_required
    def resolve_groups(self, info):
        return Group.objects.filter(members__username=self['username']).values()

    @login_required
    def resolve_attendance(self, info, **kwargs):
        logs = Log.objects.filter(member__username=self['username'])
        start = kwargs.get('startDate')
        end = kwargs.get('endDate')
        if start is not None:
            logs = logs.filter(date__gte=start)
        if end is not None:
            logs = logs.filter(date__lte=end)
        data = {'logs': logs.values(), 'avgDuration': logs.aggregate(Avg('duration'))}
        return data

    @login_required
    def resolve_isInLab(self, info):
        time = datetime.now() - timedelta(minutes=5)
        if Log.objects.filter(member__username=self['username'], lastSeen__gte=time).count() > 0:
            return True
        else:
            return False

    @login_required
    def resolve_lastSeenInLab(self, info):
        log = Log.objects.filter(member__username=self['username']).order_by('-lastSeen').values().first()
        if log is not None:
            return log['lastSeen'].astimezone(to_tz)
        else:
            return None


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        newUser = get_user_model()(
            username=username,
            email=email,
            is_active=False,
        )
        newUser.set_password(password)
        newUser.save()

        return CreateUser(user=newUser)


class userResponseObj(graphene.ObjectType):
    id = graphene.String()


class ApproveUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    Output = userResponseObj

    def mutate(self, info, username):
        if info.context.user.is_superuser:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return userResponseObj(id=user.id)
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class userChangePasswordObj(graphene.ObjectType):
    status = graphene.String()


class ChangePassword(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        newPassword = graphene.String(required=True)

    Output = userChangePasswordObj

    def mutate(self, info, password, newPassword):
        infoUser = info.context.user
        user = User.objects.values().get(username=infoUser)
        match = check_password(password, user['password'])
        if match:
            infoUser.set_password(newPassword)
            infoUser.save()
            return userChangePasswordObj(status=True)
        else:
            raise APIException('Wrong Password',
                               code='WRONG_PASSWORD')


class Query(
    dairyQuery,
    MembersQuery,
    collegeQuery,
    registrationQuery,
    attendance.schema.Query,
    activity.schema.Query,
    password.schema.Query,
    tasks.schema.Query,
    status.schema.Query,
    graphene.ObjectType
):
    user = graphene.Field(UserObj, username=graphene.String(required=True))
    users = graphene.List(UserObj, sort=graphene.String())
    isClubMember = graphene.Boolean()
    getInActiveUsers = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return User.objects.values().get(username=username)
        else:
            raise Exception('Username is a required parameter')

    def resolve_users(self, info, **kwargs):
        sort = kwargs.get('sort')
        if sort is None:
            sort = 'username'
        return User.objects.values().all().order_by(sort)

    def resolve_isClubMember(self, info, **kwargs):
        user = info.context.user
        if Profile.objects.filter(user=user).count() == 0:
            return False
        else:
            return True

    def resolve_getInActiveUsers(self, info):
        user = info.context.user
        if user.is_superuser:
            return User.objects.filter(is_active=False)
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class Mutation(membersMutation, attendance.schema.Mutation, registrationMutation, eventMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()
    approve_user = ApproveUser.Field()
    change_password = ChangePassword.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
