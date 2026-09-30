from django.urls import path
from . import views, web_views

app_name = 'analytics'

urlpatterns = [
    path('performance/', web_views.performance_page, name='performance'),
    path('recommendations/', web_views.recommendations_page, name='recommendations'),

    path('api/performance/', views.PerformanceAPIView.as_view(), name='api_performance'),
    path('api/weak-topics/', views.WeakTopicsAPIView.as_view(), name='api_weak_topics'),
    path('api/recommendations/', views.RecommendationsAPIView.as_view(), name='api_recommendations'),
]
