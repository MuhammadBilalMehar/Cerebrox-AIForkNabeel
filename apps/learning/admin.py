from django.contrib import admin
from .models import Course, Topic, AINote


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'student', 'icon', 'topic_count', 'created_at')
    list_filter = ('student',)
    search_fields = ('name', 'student__username')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created_at')
    list_filter = ('course__student',)
    search_fields = ('name',)


@admin.register(AINote)
class AINoteAdmin(admin.ModelAdmin):
    list_display = ('topic', 'student', 'study_level', 'created_at')
    list_filter = ('study_level',)
