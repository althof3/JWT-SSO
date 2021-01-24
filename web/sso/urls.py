

from django.urls import path, include
from .views import *
from rest_framework_jwt.views import obtain_jwt_token

from .cas_wrapper import APILoginView, APILogoutView

urlpatterns = [
    path('login/', APILoginView.as_view(), name='login'),
    path('logout/', APILogoutView.as_view(), name='logout'),
    path('token-auth/', obtain_jwt_token),
    # path('register/supervisor-lembaga/', UserRegistrationView.as_view(), name='register-supervisor-lembaga'),
    # path('login/supervisor-lembaga/', UserLoginView.as_view(), name='login-supervisor-lembaga'),
    path('profile/', ProfileDashboardView.as_view(), name='profile'),
]
