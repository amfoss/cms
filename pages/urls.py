from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
]