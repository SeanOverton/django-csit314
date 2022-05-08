from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import CustomUser as User
from .models import RoadsideCallout, UserSubscriptions, UserLocation
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'user_type', 'image')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        # Ensuring the usertype is valid.
        if attrs['user_type'] not in ['customer', 'mechanic']:
            raise serializers.ValidationError({"user_type": "User type is not a valid type, a mechanic or customer."})

        return attrs

    def create(self, validated_data):
        if validated_data.get('image', None):
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                user_type=validated_data['user_type'],
                image=validated_data['image'],
            )
        else:
            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                user_type=validated_data['user_type'],
            )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        # only allows you to update username and password
        instance.username = self.validated_data.get('username', instance.username)
        instance.first_name = self.validated_data.get('first_name', instance.first_name)
        instance.last_name = self.validated_data.get('last_name', instance.last_name)
        
        # instance.image = self.validated_data.get('image', instance.image)
        
        # if validated_data['password']:
        #     instance.set_password(validated_data['password'])
        instance.save()
        
        return instance

# create callout requests
class CalloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadsideCallout
        fields = ('username', 'status', 'location', 'description', 'mechanic', 'date', 'rating', 'review')
        validators = [
            UniqueTogetherValidator(
                queryset=RoadsideCallout.objects.all(),
                fields=['username', 'location']
            )
        ]

    def validate(self, attrs):
        if attrs['status'] not in ['PENDING', 'ACCEPTED', 'COMPLETED', 'REVIEWED', 'CANCELLED']:
            raise serializers.ValidationError({"status": "Invalid Status. Use instead: ['PENDING', 'ACCEPTED', 'COMPLETED', 'REVIEWED', 'CANCELLED']"})

        return attrs

    def create(self, validated_data):
        return RoadsideCallout.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.username = self.validated_data.get('username', instance.username)
        instance.status = self.validated_data.get('status', instance.status)
        # instance.location = self.validated_data.get('location', instance.location)
        # instance.description = self.validated_data.get('description', instance.description)
        instance.mechanic = self.validated_data.get('mechanic', instance.mechanic)
        # instance.date = self.validated_data.get('date', instance.date)
        instance.rating = self.validated_data.get('rating', instance.rating)
        instance.review = self.validated_data.get('review', instance.review)
        instance.save()
        return instance

# add a subscription car
class UserSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptions
        fields = ('username', 'vehicle_registration', 'vehicle_type', 'vehicle_model', 'vehicle_brand', 'vehicle_year', 'vehicle_weight', 'active')
    
    def create(self, validated_data):
        return UserSubscriptions.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = self.validated_data.get('username', instance.username)
        instance.vehicle_registration = self.validated_data.get('vehicle_registration', instance.vehicle_registration)
        instance.active = self.validated_data.get('active', instance.active)
        instance.save()
        return instance

# create callout requests
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ('username', 'location')
        validators = [
            UniqueTogetherValidator(
                queryset=UserLocation.objects.all(),
                fields=['username']
            )
        ]

    def validate(self, attrs):
        if list(attrs['location'].keys()) != ["lat", "lng"]:
            raise serializers.ValidationError({"location": "Invalid Location JSON keys. JSON must be in format {'lat': 0, 'lng': 0}"})

        return attrs

    def create(self, validated_data):
        return UserLocation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.location = self.validated_data.get('location', instance.location)
        instance.save()
        return instance