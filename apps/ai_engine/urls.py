from django.urls import path
from .views import GenerateNotesAPIView, GenerateMCQAPIView

app_name = 'ai_engine'

urlpatterns = [
    path('notes/generate/', GenerateNotesAPIView.as_view(), name='generate_notes'),
    path('mcq/generate/', GenerateMCQAPIView.as_view(), name='generate_mcq'),
]
