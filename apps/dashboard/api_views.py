from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.analytics.performance import student_overview


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        overview = student_overview(request.user)
        overview.pop('recent_quizzes', None)
        return Response(overview)
