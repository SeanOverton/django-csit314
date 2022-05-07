from django.test import TestCase
from .models import RoadsideCallout

class CalloutTestCase(TestCase):
    def setUp(self):
        RoadsideCallout.objects.create(username="test", 
                                        status="roar",
                                        location="an address",
                                        description="description")

    def test_callouts_have_correct_data(self):
        callout = RoadsideCallout.objects.get(username="test")
        self.assertEqual(callout.status, "roar")
        self.assertEqual(callout.location, "an address")
        self.assertEqual(callout.description, "description")

    # maybe this should be a serializer test seperate from the models test
    def test_callouts_update_correctly(self):
        callout = RoadsideCallout.objects.get(username="test")
        self.assertEqual(callout.status, "roar")
        self.assertEqual(callout.location, "an address")
        self.assertEqual(callout.description, "description")
