from rest_framework import serializers
from .models import Person
from registration.models import AppUser

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'phone', 'email', 'slug', 'qr_code']

class PersonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'email', 'phone', 'slug', 'qr_code']

class AppUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['full_name', 'email', 'slug']
