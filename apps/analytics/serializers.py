from rest_framework import serializers


class TopicPerformanceSerializer(serializers.Serializer):
    topic__id = serializers.IntegerField()
    topic__name = serializers.CharField()
    topic__course__name = serializers.CharField()
    avg_score = serializers.FloatField()
    attempts = serializers.IntegerField()
    status = serializers.CharField(required=False)


class RecommendationSerializer(serializers.Serializer):
    topic = serializers.CharField()
    score = serializers.FloatField()
    status = serializers.CharField()
    message = serializers.CharField()
