from sso.models import Profile
from sso.utils import update_profile
from django.contrib.auth.models import User
from .serializers import (ProfileSerializer)
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

from django_cas_ng import views as cas_views
from django_cas_ng.models import ProxyGrantingTicket, SessionTicket
from django_cas_ng.utils import get_protocol, get_redirect_url, get_cas_client
from django_cas_ng.signals import cas_user_logout
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework_jwt.settings import api_settings



JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def halo(request):

    user = request.user


    # create jwt token
    payload = JWT_PAYLOAD_HANDLER(user)
    # print(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    
    attributes = request.session.get('attributes', {})

    update_profile(user, attributes)

    return render(request, 'sso/token.html', {'token':jwt_token})


class ProfileDashboardView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        user_data = Profile.objects.get(user=request.user)
        # status_code = status.HTTP_200_OK
        serializer = ProfileSerializer(user_data)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class APILogoutView(cas_views.LogoutView):


    """
    Redirects to CAS logout page


    :param request:
    :return:
    """
    
    def get(self, request: HttpRequest) -> HttpResponse:
        next_page = settings.SUCCESS_SSO_AUTH_REDIRECT

        try:
            del request.session['token']
        except KeyError:
            pass

        # try to find the ticket matching current session for logout signal
        try:
            st = SessionTicket.objects.get(session_key=request.session.session_key)
            ticket = st.ticket
        except SessionTicket.DoesNotExist:
            ticket = None
        # send logout signal
        cas_user_logout.send(
            sender="manual",
            user=request.user,
            session=request.session,
            ticket=ticket,
        )

        # clean current session ProxyGrantingTicket and SessionTicket
        ProxyGrantingTicket.objects.filter(session_key=request.session.session_key).delete()
        SessionTicket.objects.filter(session_key=request.session.session_key).delete()
        auth_logout(request)


        next_page = next_page or get_redirect_url(request)
        if settings.CAS_LOGOUT_COMPLETELY:
            client = get_cas_client(request=request)
            return HttpResponseRedirect(client.get_logout_url(next_page))


        # This is in most cases pointless if not CAS_RENEW is set. The user will
        # simply be logged in again on next request requiring authorization.
        return HttpResponseRedirect(next_page)