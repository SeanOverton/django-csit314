from django.test import TestCase
from .models import RoadsideCallout, UserSubscriptions, UserLocation, CustomUser
from .serializers import UserSubscriptionsSerializer, CalloutSerializer, LocationSerializer
import json

"""
Models tests
"""

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

class UserSubscriptionTestCase(TestCase):
    def setUp(self):
        UserSubscriptions.objects.create(username = "username",
                                        vehicle_registration = "ABC123",
                                        vehicle_type = "vehicle_type",
                                        vehicle_model = "vehicle_model",
                                        vehicle_brand = "vehicle_brand",
                                        vehicle_year = "2000",
                                        vehicle_weight = "vehicle_weight",
                                        active = True
                                        )

    def test_subscription_have_correct_data(self):
        user_subscription = UserSubscriptions.objects.get(username="username")
        self.assertEqual(user_subscription.vehicle_registration, "ABC123")
        self.assertEqual(user_subscription.vehicle_model, "vehicle_model")
        self.assertEqual(user_subscription.vehicle_brand, "vehicle_brand")
        self.assertEqual(user_subscription.vehicle_year, "2000")
        self.assertEqual(user_subscription.vehicle_weight, "vehicle_weight")
        self.assertEqual(user_subscription.active, True)

class UserLocationTestCase(TestCase):
    def setUp(self):
        UserLocation.objects.create(username = "username",
                                location = {"lat": 0, "lng": 0}
                                    )

    def test_location_have_correct_data(self):
        user_location = UserLocation.objects.get(username="username")
        self.assertEqual(user_location.username, "username")
        self.assertEqual(user_location.location, {"lat": 0, "lng": 0})

class CustomerUserTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(username = "username",
                                user_type = "customer",
                                password="test12345",
                                email="user@email.com",
                                first_name="Johnny",
                                last_name="Smith"
                                )

    def test_customuser_have_correct_data(self):
        user = CustomUser.objects.get(username="username")
        self.assertEqual(user.username, "username")
        self.assertEqual(user.user_type, "customer")
        self.assertEqual(user.password, "test12345")
        self.assertEqual(user.email, "user@email.com")
        self.assertEqual(user.first_name, "Johnny")
        self.assertEqual(user.last_name, "Smith")

"""
Serializer tests:
For testing django-rest-framework serializers referenced
https://www.vinta.com.br/blog/2017/how-i-test-my-drf-serializers/
"""

class CalloutSerializerTestCase(TestCase):
    def setUp(self):
        self.callout_attributes = {
            "username": "John", 
            "status": "PENDING",
            "location": "an address",
            "description": "description",
            "mechanic": "Joey",
            "rating": "5",
            "review": "Great service"
        }

        self.serializer_data = {
            "username": "John", 
            "status": "PENDING",
            "location": "an address",
            "description": "description",
            "mechanic": "Joey",
            "rating": 5,
            "review": "Great service"
        }

        self.callout = RoadsideCallout.objects.create(**self.callout_attributes)
        self.serializer = CalloutSerializer(instance=self.callout)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        keys = ["username", 
                "status", 
                "location",
                "description",
                "mechanic",
                "date",
                "rating",
                "review"]

        self.assertCountEqual(data.keys(), keys)
    
    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["username"], self.callout_attributes["username"])
    
    def test_status_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["status"], self.callout_attributes["status"])
    
    def test_location_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["location"], self.callout_attributes["location"])

    def test_description_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["description"], self.callout_attributes["description"])

    def test_mechanic_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["mechanic"], self.callout_attributes["mechanic"])

    def test_rating_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["rating"], self.callout_attributes["rating"])

    def test_review_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["review"], self.callout_attributes["review"])

    def test_status_field_bounds(self):
        self.serializer_data["status"] = "INVALID_STATUS"
        serializer = CalloutSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        # checks the error is an error with the status
        self.assertEqual(set(serializer.errors), set(["status"]))

    def test_rating_field_bounds(self):
        self.serializer_data["rating"] = 11
        serializer = CalloutSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        # checks the error is an error with the status
        self.assertEqual(set(serializer.errors), set(["rating"]))

    def test_update_status_field_with_valid_data(self):
        self.serializer_data["status"] = "ACCEPTED"
        self.serializer_data["location"] = "new_location"

        serializer = CalloutSerializer(data=self.serializer_data)
        
        if serializer.is_valid():
            new_callout = serializer.save()
        else:
            print(serializer.errors)
        new_callout.refresh_from_db()

        self.assertEqual(new_callout.status, "ACCEPTED")

class UserSubscriptionSerializerTestCase(TestCase):
    def setUp(self):
        self.subscription_attributes = {
            "username": "John", 
            "vehicle_registration": "ABC123",
            "vehicle_type": "Fast car", 
            "vehicle_model": "Speedy1000", 
            "vehicle_brand": "Need4Speed", 
            "vehicle_year": "2000", 
            "vehicle_weight": "1800", 
            "active": True
        }

        self.serializer_data = {
            "username": "John", 
            "vehicle_registration": "ABC123",
            "vehicle_type": "Fast car", 
            "vehicle_model": "Speedy1000", 
            "vehicle_brand": "Need4Speed", 
            "vehicle_year": "2000", 
            "vehicle_weight": "1800", 
            "active": True
        }

        self.subscription = UserSubscriptions.objects.create(**self.subscription_attributes)
        self.serializer = UserSubscriptionsSerializer(instance=self.subscription)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        keys = ["username",
                "vehicle_registration", 
                "vehicle_type", 
                "vehicle_model", 
                "vehicle_brand", 
                "vehicle_year", 
                "vehicle_weight", 
                "active"]

        self.assertCountEqual(data.keys(), keys)
    
    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["username"], self.subscription_attributes["username"])
    
    def test_vehicle_registration_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_registration"], self.subscription_attributes["vehicle_registration"])
    
    def test_vehicle_type_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_type"], self.subscription_attributes["vehicle_type"])

    def test_vehicle_model_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_model"], self.subscription_attributes["vehicle_model"])

    def test_vehicle_brand_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_brand"], self.subscription_attributes["vehicle_brand"])

    def test_vehicle_year_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_year"], self.subscription_attributes["vehicle_year"])

    def test_vehicle_weight_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["vehicle_weight"], self.subscription_attributes["vehicle_weight"])

    def test_active_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["active"], self.subscription_attributes["active"])

    def test_vehicle_registration_field_bounds(self):
        self.serializer_data["vehicle_registration"] = "INVALID_REGO"
        serializer = UserSubscriptionsSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(["vehicle_registration"]))

    def test_active_field_bounds(self):
        self.serializer_data["active"] = "ACTIVE"
        serializer = UserSubscriptionsSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(["active"]))

    def test_active_field_with_valid_data(self):
        self.serializer_data["active"] = False

        serializer = UserSubscriptionsSerializer(data=self.serializer_data)
        
        serializer.is_valid()
        new_subscription = serializer.save()
        new_subscription.refresh_from_db()

        self.assertEqual(new_subscription.active, False)

class LocationSerializerTestCase(TestCase):
    def setUp(self):
        self.location_attributes = {
            "username": "JohnSmith", 
            "location": {"lat": 0, "lng": 0}
        }

        self.serializer_data = {
            "username": "JohnSmith", 
            "location": {"lat": 0, "lng": 0}
        }

        self.location = UserLocation.objects.create(**self.location_attributes)
        self.serializer = LocationSerializer(instance=self.location)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        keys = ["username", 
                "location"]

        self.assertCountEqual(data.keys(), keys)
    
    def test_username_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["username"], self.location_attributes["username"])
    
    def test_location_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["location"], self.location_attributes["location"])
    
    def test_location_field_bounds(self):
        self.serializer_data["username"] = "new_username1"
        self.serializer_data["location"] = {"lat": 1}
        serializer = LocationSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(["location"]))

    def test_location_field_with_valid_data_update(self):
        self.serializer_data["username"] = "new_username2"
        self.serializer_data["location"] = {"lat":-31, "lng": 50}

        serializer = LocationSerializer(data=self.serializer_data)
        
        if serializer.is_valid():
            new_userlocation = serializer.save()
            new_userlocation.refresh_from_db()
        else:
            print(serializer.errors)

        self.assertEqual(new_userlocation.location, {"lat":-31, "lng": 50})