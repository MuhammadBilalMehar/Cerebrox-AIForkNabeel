from django.urls import path
from .api_views import RegisterAPIView, LoginAPIView, LogoutAPIView, MeAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
    path('me/', MeAPIView.as_view(), name='api_me'),
]
