from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from members.models import *
from activity.models import *
from gsoc.models import *
from blog.models import *
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
import json
from datetime import datetime

class UserProfile(DetailView):
    model = User
    template_name = 'member/profile.haml'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_interests(self, profile):
        interests = []
        for i in profile.interests.all():
            interests.append(i)
        return interests

    def get_expertise(self, profile):
        expertise = []
        for i in profile.expertise.all():
            expertise.append(i)
        return expertise

    def get_activity(self, member):
        att = Attendance.objects.filter(member=member)
        a = {}
        for i in att:
            a[str(int(i.session_start.timestamp()))] = int(i.duration.seconds/(60*60))
        return a


    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.get_object())
            context['profile'] = profile
            context['activity'] = self.get_activity(member=self.get_object())
            context['socialProfiles'] = SocialProfile.objects.filter(profile=profile)
            context['certificates'] = Certificate.objects.filter(member=self.get_object())
            context['publications'] = Publication.objects.filter(members=self.get_object())
            context['honours'] = Honour.objects.filter(member=self.get_object())
            context['courses'] = Course.objects.filter(member=self.get_object())
            context['talks'] = Talk.objects.filter(member=self.get_object())
            context['workExperience'] = WorkExperience.objects.filter(profile=profile)
            context['interests'] = self.get_interests(profile)
            context['expertise'] = self.get_expertise(profile)
            context['posts'] = Post.objects.filter(author=self.get_object())
            context['projects'] = Project.objects.filter(members=self.get_object())
            context['educationalQualification'] = EducationalQualification.objects.filter(profile=profile)

        except Profile.DoesNotExist:
            context['error'] = 'No data found for this user!'
        return context

class Achievements(ListView):
    model = User
    template_name = 'activity/achievements.haml'

    def get_gsoc_members(self,gsocs):
        members = []
        for i in gsocs:
            if not any(d['username'] == i.member.username for d in members):
                members.append(dict(username=i.member.username,avatar=i.member.Profile.avatar,count=1))
            else:
                for m in members:
                    if m['username'] == i.member.username:
                        m.update(count=m['count']+1)
        return members

    def get_gsoc_orgs(self,gsocs):
        orgs = []
        for i in gsocs:
            if not any(d['id'] == i.organisation.id for d in orgs):
                orgs.append(dict(name=i.organisation.name,icon=i.organisation.icon,id=i.organisation.id,count=1))
            else:
                for m in orgs:
                    if m['name'] == i.organisation.name:
                        m.update(count=m['count']+1)
        return orgs

    def get_gsoc_stipend(self):
         c = GSoC.objects.filter(status='C').count()
         s = GSoC.objects.filter(status='2').count()
         f = GSoC.objects.filter(status='1').count()
         return int((f*0.3*3) + (s*0.6*3) + (c*3))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['internships'] = Event.objects.filter(type='I')
        context['international_events'] = Event.objects.filter(international=True)
        context['talks'] = Talk.objects.all()
        context['publications'] = Publication.objects.all()
        gsocs = GSoC.objects.filter(status__in=['C','S','1','2','3'])
        context['gsoc_members'] = self.get_gsoc_members(gsocs)
        context['current_gsoc'] = GSoC.objects.filter(status__in=['C','S','1','2','3'], year=2018)
        context['gsoc_orgs'] = self.get_gsoc_orgs(gsocs)
        context['gsoc_stipend'] = self.get_gsoc_stipend()
        return context

class Members(ListView):
    model = User
    template_name = 'member/list.haml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        return context


class Blog(ListView):
    model = Post
    template_name = 'blog/list.haml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(featured=True)
        return context

class BlogPost(DetailView):
    model = Post
    template_name = 'blog/single.haml'

    def get_context_data(self, **kwargs):
        context = super(BlogPost, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['username'])
        try:
            context['post'] = Post.objects.get(author=user,slug=self.kwargs['slug'])
        except Profile.DoesNotExist:
            context['error'] = 'No data found for this post!'
        return context

class Projects(ListView):
    model = Project
    template_name = 'project/list.haml'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(featured=True)
        return context

class ProjectDetail(DetailView):
    model = Project
    template_name = 'project/project.haml'

    def get_team(self,project):
        team = []
        for m in project.members.all():
            team.append(Profile.objects.get(user=m))
        return team

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        try:
            project = Project.objects.get(slug=self.kwargs['slug'])
            context['project'] = project
            context['team'] = self.get_team(project)
            context['socialProfiles'] = ProjectLink.objects.filter(project=project)
        except Profile.DoesNotExist:
            context['error'] = 'No data found for this project!'
        return context

class HomePage(TemplateView):
    template_name = "home.haml"

class AboutPage(TemplateView):
    template_name = "about/about.haml"

class ClubLifePage(TemplateView):
    template_name = "about/life.haml"