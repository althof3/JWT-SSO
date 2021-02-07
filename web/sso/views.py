from sso.models import Profile
from sso.utils import update_profile
from django.contrib.auth.models import User
from .serializers import (UserSerializer, UserLoginSerializer, ProfileSerializer)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

def halo(request, **kwargs):

    user = request.user


    # create jwt token
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    
    attributes = request.session.get('attributes', {})

    update_profile(user, attributes)

    return render(request, 'sso/token.html', {'token':jwt_token})

class UserLoginView(RetrieveAPIView):  # pragma: no cover


    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            'token': serializer.data['token'],
        }


        return Response(response, status=status.HTTP_200_OK)

class ProfileDashboardView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        print(request.user.email)
        user_data = Profile.objects.get(user=request.user)
        # status_code = status.HTTP_200_OK
        serializer = ProfileSerializer(user_data)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)


class UserProfileUserView(RetrieveAPIView):  # pragma: no cover


    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication


    def get(self, request):
        # print(request.user.email)
        user_data = User.objects.get(email=request.user.email)
        status_code = status.HTTP_200_OK
        serializer = UserSerializer(user_data, context=serializer_context)
        response = {
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)