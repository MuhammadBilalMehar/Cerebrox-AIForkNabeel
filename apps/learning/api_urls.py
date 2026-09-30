from rest_framework.routers import DefaultRouter
from .api_views import CourseViewSet, TopicViewSet, AINoteViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('topics', TopicViewSet, basename='topic')
router.register('notes', AINoteViewSet, basename='ainote')

urlpatterns = router.urls
