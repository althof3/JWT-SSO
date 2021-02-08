
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    """User serializer json field."""


    full_name = serializers.CharField(source='get_full_name')


    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'full_name']

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'
