from django.urls import path
from . import views as api_views
from . import web_views

app_name = 'quizzes'

urlpatterns = [
    # student-facing (server-rendered) flow
    path('generate/', web_views.quiz_dashboard, name='dashboard_generate'),
    path('topic/<int:topic_id>/generate/', web_views.quiz_generate, name='generate'),
    path('<int:quiz_id>/take/', web_views.quiz_take, name='take'),
    path('<int:quiz_id>/submit/', web_views.quiz_submit, name='submit'),
    path('<int:quiz_id>/result/', web_views.quiz_result, name='result'),
    path('history/', web_views.quiz_history, name='history'),

    # JSON API
    path('api/generate/', api_views.GenerateQuizAPIView.as_view(), name='api_generate'),
    path('api/<int:pk>/submit/', api_views.SubmitQuizAPIView.as_view(), name='api_submit'),
    path('api/<int:pk>/', api_views.QuizDetailAPIView.as_view(), name='api_detail'),
]
