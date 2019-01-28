import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

new_group, created = Group.objects.get_or_create(name='self_viewers')