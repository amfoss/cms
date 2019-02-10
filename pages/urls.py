from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('achievements/', Achievements.as_view(), name='home_page'),
    url(r'^@(?P<username>[\w.@+-]+)/$', UserProfile.as_view(), name="user")
]