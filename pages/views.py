from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from members.models import *
from activity.models import *
from gsoc.models import *
from django.contrib.auth.models import User
from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404


class UserProfile(DetailView):
    model = User
    template_name = 'members/profile.haml'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        try:
            profile = get_object_or_404(Profile, user=self.get_object())
            context['profile'] = profile
            context['socialProfiles'] = SocialProfile.objects.filter(profile=profile)
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
    template_name = 'members/list.haml'

class Blog(ListView):
    model = User
    template_name = 'blog/blog.haml'

class HomePage(TemplateView):
    template_name = "home.haml"

class AboutPage(TemplateView):
    template_name = "about/about.haml"
