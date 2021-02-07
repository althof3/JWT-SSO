# from rest_framework import serializers
# from rest_framework_jwt.settings import api_settings
# from django.contrib.auth.models import User

# from web.sso.cas_wrapper import JWT_ENCODE_HANDLER, JWT_PAYLOAD_HANDLER
from django.db.models import fields
from sso.cas_wrapper import JWT_ENCODE_HANDLER, JWT_PAYLOAD_HANDLER
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
        


class UserLoginSerializer(serializers.Serializer):
    """Serializer json field for login."""


    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        try:
            email = User.objects.get(username=username)
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError(
                    'User with given email and password does not exists'
                )
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            username = user.username
            return {
                'username': user.username,
                'token': jwt_token
            }
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )