from sso.models import Profile
from django.contrib.auth.models import User
from .serializers import (UserSerializer, UserLoginSerializer, ProfileSerializer)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

# factory = APIRequestFactory()
# request = factory.get('/')


# serializer_context = {
#     'request': Request(request),
# }

# response_field = ['success', 'status_code', 'message']
# profile_success_message = 'User profile fetched successfully'

# class UserRegistrationView(CreateAPIView):  # pragma: no cover


#     permission_classes = (AllowAny,)
#     serializer_class = SupervisorLembagaRegistrationSerializer


#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         status_code = status.HTTP_201_CREATED
#         response = {
#             response_field[0]: 'True',
#             response_field[1]: status_code,
#             response_field[2]: 'User registered successfully',
#         }


#         return Response(response, status=status.HTTP_201_CREATED)


class UserLoginView(RetrieveAPIView):  # pragma: no cover


    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            # response_field[0]: 'True',
            # response_field[1]: status_code,
            # response_field[2]: 'User logged in successfully',
            'token': serializer.data['token'],
        }


        return Response(response, status=status.HTTP_200_OK)

class ProfileDashboardView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    # serializer_class = ProfileSerializer
    authentication_class = JSONWebTokenAuthentication

    # print("hahaha")

    def get(self, request):
        print(request.user.email)
        user_data = Profile.objects.get(user=request.user)
        # status_code = status.HTTP_200_OK
        serializer = ProfileSerializer(user_data)
        response = {
            # response_field[0]: 'true',
            # response_field[1]: status_code,
            # response_field[2]: profile_success_message,
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
            # response_field[0]: 'true',
            # response_field[1]: status_code,
            # response_field[2]: profile_success_message,
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)