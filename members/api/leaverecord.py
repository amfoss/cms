import graphene
from framework.api.user import UserBasicObj
from django.contrib.auth.models import User
from members.models import LeaveRecord
from datetime import date, datetime

class LeaveRecordObj(graphene.ObjectType):
    member = graphene.Field(UserBasicObj)
    approver = graphene.Field(UserBasicObj)
    startDate = graphene.types.datetime.Date(required=True)
    endDate = graphene.types.datetime.Date(required=True)
    reason = graphene.String()
    
    def resolve_member(self,info):
        return  User.objects.values().get(id=self['member_id'])

class getLeaveRecordsObj(graphene.ObjectType):
    leaveRecords = graphene.List(LeaveRecordObj)
    
    def resolve_leaveRecords(self, info):
        return self['leaveRecords']

class Query(object):
    getLeaveRecords = graphene.Field(
        getLeaveRecordsObj,
        startDate = graphene.Date(required=True),
        endDate = graphene.Date()
    )
    leaveRecords = graphene.List(LeaveRecordObj)
    

    def resolve_getLeaveRecords(self, info, **kwargs):
        startDate = kwargs.get('startDate')
        endDate = kwargs.get('endDate')
        
        leaveRecords = LeaveRecord.objects.values().all()
        
        if startDate is not None:
            leaveRecords = leaveRecords.filter(start_date__gte=startDate)
        else:
            raise Exception('StartDate is required')
        if endDate is not None:
            leaveRecords = leaveRecords.filter(end_date__lte=endDate)
        else:
            endDate = date.today()
        
        data = {
            'leaveRecords': leaveRecords.values()
        }
        return data
        
    def resolve_leaveRecords(self, info, **kwargs):
        return LeaveRecord.objects.values().all()
