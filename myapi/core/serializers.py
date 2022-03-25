from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import CustomUser as User
from .models import RoadsideCallout
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
        #need to add type of user ie. mechanic or not? and also subscription or not?
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type']
        )
 
        user.set_password(validated_data['password'])
        user.save()

        return user

# create callout requests
class CalloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadsideCallout
        fields = ('username', 'status', 'location', 'mechanic', 'date', 'rating', 'review')
        validators = [
            UniqueTogetherValidator(
                queryset=RoadsideCallout.objects.all(),
                fields=['username', 'date']
            )
        ]

    def validate(self, attrs):
        # if attrs['password'] != attrs['password2']:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        return RoadsideCallout.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = self.validated_data.get('username', instance.username)
        instance.status = self.validated_data.get('status', instance.status)
        instance.location = self.validated_data.get('location', instance.location)
        instance.mechanic = self.validated_data.get('mechanic', instance.mechanic)
        instance.date = self.validated_data.get('date', instance.date)
        instance.rating = self.validated_data.get('rating', instance.rating)
        instance.review = self.validated_data.get('review', instance.review)
        instance.save()
        return instance

# for next serializers. https://www.django-rest-framework.org/tutorial/1-serialization/

# view all callout requests

# accept a callout request

# mark a callout as complete

# review a complete callout

# get average reviews 

# add a subscription car