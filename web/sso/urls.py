

from django.urls import path, include
from .views import *
from rest_framework_jwt.views import obtain_jwt_token

from .cas_wrapper import APILoginView, APILogoutView

app_name = 'sso'

urlpatterns = [
    path('login/', APILoginView.as_view(), name='login'),
    path('logout/', APILogoutView.as_view(), name='logout'),
    path('token-auth/', obtain_jwt_token),
    
    path('profile/', ProfileDashboardView.as_view(), name='profile'),
    path("halo/", halo, name="halo")
]
