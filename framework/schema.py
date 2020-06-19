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
import activity.schema
from dairy.schema import Query as dairyQuery
from registration.schema import Mutation as registrationMutation, Query as registrationQuery
import tasks.schema
import status.schema
import password.schema
from .api.APIException import APIException
from dairy.schema import Mutation as eventMutation

from members.schema import Query as MembersQuery, Mutation as membersMutation
from members.api.profile import ProfileObj
from members.api.group import GroupObj
from members.models import Profile, Group

from attendance.models import Log
from attendance.api.log import userAttendanceObj

from .api.user import UserBasicObj
from .api.mutation import Mutation as PlatformMutation

import secrets,string

from framework import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from_email = settings.EMAIL_HOST_USER

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

    def resolve_profile(self, info):
        return Profile.objects.values().get(user__username=self['username'])

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


class userStatusObj(graphene.ObjectType):
    status = graphene.String()


class ChangePassword(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        newPassword = graphene.String(required=True)

    Output = userStatusObj

    def mutate(self, info, password, newPassword):
        infoUser = info.context.user
        user = User.objects.values().get(username=infoUser)
        match = check_password(password, user['password'])
        if match:
            infoUser.set_password(newPassword)
            infoUser.save()
            return userStatusObj(status=True)
        else:
            raise APIException('Wrong Password',
                               code='WRONG_PASSWORD')


class UpdateProfile(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        firstName = graphene.String()
        lastName = graphene.String()
        email = graphene.String()
        phoneNo = graphene.String()
        githubUsername = graphene.String()
        gitlabUsername = graphene.String()
        customEmail = graphene.String()
        roll = graphene.String()
        batch = graphene.Int()
        about = graphene.String()

    Output = userResponseObj

    def mutate(self, info, username=None, firstName=None, lastName=None, email=None, phoneNo=None,
               githubUsername=None, gitlabUsername=None, customEmail=None, roll=None, batch=None, about=None):
        user = info.context.user
        profile = Profile.objects.get(user=user)
        if username is not None:
            user.username = username
        if firstName is not None:
            user.first_name = firstName
            profile.first_name = firstName
        if lastName is not None:
            user.last_name = lastName
            profile.last_name = lastName
        if email is not None:
            user.email = email
            profile.email = email
        if phoneNo is not None:
            profile.phone = phoneNo
        if githubUsername is not None:
            profile.githubUsername = githubUsername
        if gitlabUsername is not None:
            profile.gitlabUsername = gitlabUsername
        if customEmail is not None:
            profile.customEmail = customEmail
        if roll is not None:
            profile.roll_number = roll
        if batch is not None:
            profile.batch = batch
        if about is not None:
            profile.about = about
        user.save()
        profile.save()
        return userResponseObj(id=user.id)

class ResetPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    Output = userStatusObj

    def mutate(self, info, email):
        user = User.objects.get(email=email)
        if user is not None:
            newPassword = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))
            user.set_password(newPassword)
            user.save()
            context = {
                "password" : newPassword,
                "username" : user.username
            }
            message = render_to_string('email/password_reset_email.html', context)
            send_mail('Reset Password | amFOSS CMS',  strip_tags(message) , from_email, [email], fail_silently=False, html_message=message)
            return userStatusObj(status=True)
        else:
            raise APIException('Email is not registered',
                               code='WRONG_EMAIL')

class Query(
    dairyQuery,
    MembersQuery,
    registrationQuery,
    attendance.schema.Query,
    password.schema.Query,
    tasks.schema.Query,
    activity.schema.Query,
    status.schema.Query,
    graphene.ObjectType
):
    user = graphene.Field(UserObj, username=graphene.String(required=True))
    users = graphene.List(UserObj, sort=graphene.String())
    activeUsers = graphene.List(UserObj, sort=graphene.String())
    isClubMember = graphene.Boolean()
    isAdmin = graphene.Boolean()
    inActiveUsers = graphene.List(UserObj, sort=graphene.String())

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

    def resolve_activeUsers(self, info, **kwargs):
        sort = kwargs.get('sort')
        if sort is None:
            sort = 'username'
        return User.objects.values().filter(is_active=True).order_by(sort)

    def resolve_isClubMember(self, info, **kwargs):
        user = info.context.user
        if Profile.objects.filter(user=user).count() == 0:
            return False
        else:
            return True

    def resolve_isAdmin(self, info):
        if info.context.user.is_superuser:
            return True
        else:
            return False

    def resolve_inActiveUsers(self, info, **kwargs):
        sort = kwargs.get('sort')
        if sort is None:
            sort = 'username'
        if info.context.user.is_superuser:
            return User.objects.values().filter(is_active=False).order_by(sort)
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')


class Mutation(membersMutation, attendance.schema.Mutation, registrationMutation, eventMutation, PlatformMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    create_user = CreateUser.Field()
    approve_user = ApproveUser.Field()
    change_password = ChangePassword.Field()
    UpdateProfile = UpdateProfile.Field()
    reset_password = ResetPassword.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
