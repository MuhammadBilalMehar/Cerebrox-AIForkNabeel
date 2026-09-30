from rest_framework import serializers


class NotesGenerateSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    length = serializers.ChoiceField(choices=['short', 'medium', 'long'], default='medium')


class MCQGenerateSerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    difficulty = serializers.ChoiceField(choices=['Easy', 'Medium', 'Hard'], default='Medium')
    count = serializers.IntegerField(min_value=1, max_value=25, default=10)
