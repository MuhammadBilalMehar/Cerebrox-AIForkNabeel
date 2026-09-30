from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_quizzes = serializers.IntegerField()
    average_score = serializers.FloatField()
    highest_score = serializers.FloatField()
    lowest_score = serializers.FloatField()
