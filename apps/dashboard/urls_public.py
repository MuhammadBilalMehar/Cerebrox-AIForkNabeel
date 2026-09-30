from django.urls import path
from . import views_public as v

app_name = 'public'

urlpatterns = [
    path('', v.landing, name='landing'),
    path('about/', v.about, name='about'),
]
