from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('about/', AboutPage.as_view(), name='about_page'),
    path('life/', ClubLifePage.as_view(), name='club_life'),
    path('achievements/', Achievements.as_view(), name='achievements'),
    path('members/', Members.as_view(), name='members'),
    path('blog/', Blog.as_view(), name='blog'),
    path('projects/', Projects.as_view(), name='projects'),
    url(r'^project/(?P<slug>[\w.@+-]+)/$', ProjectDetail.as_view(), name="project"),
    url(r'^@(?P<username>[\w.@+-]+)/$', UserProfile.as_view(), name="profile"),
    url(r'^@(?P<username>[\w.@+-]+)/(?P<slug>[\w.@+-]+)$', BlogPost.as_view(), name="post"),
]
