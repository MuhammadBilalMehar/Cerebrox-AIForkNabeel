from rest_framework import serializers
from .models import Course, Topic, AINote


class TopicSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Topic
        fields = ('id', 'course', 'course_name', 'name', 'description', 'created_at', 'updated_at')


class CourseSerializer(serializers.ModelSerializer):
    topic_count = serializers.ReadOnlyField()
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'icon', 'topic_count', 'topics', 'created_at', 'updated_at')


class AINoteSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source='topic.name', read_only=True)

    class Meta:
        model = AINote
        fields = ('id', 'topic', 'topic_name', 'study_level', 'content', 'created_at')
        read_only_fields = ('content', 'study_level', 'created_at')
