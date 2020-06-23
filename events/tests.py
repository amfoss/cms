from django.test import TestCase
from datetime import datetime
from .models import Event


class EventTest(TestCase):

    def setUp(self):
        Event.objects.create(
            name = "The Open Talks 2020",
            slug = "open-talks",
            content = "The open talks 2020 was conducted on Februaury 15 by amFOSS in Amritapuri"
        )

    def test_event_fields(self):
        events = Event.objects.get(name="The Open Talks 2020")

        self.assertEquals(events.name,'The Open Talks 2020')
        self.assertEquals(events.slug,'open-talks')
        self.assertEquals(events.content,'The open talks 2020 was conducted on Februaury 15 by amFOSS in Amritapuri')
