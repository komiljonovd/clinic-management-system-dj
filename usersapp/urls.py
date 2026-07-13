from django.urls import path
from usersapp.views.register_views import RegisterAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 



urlpatterns = [
    path('user/',RegisterAPI.as_view(),name='register'),
    path('user/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),



]