from django.contrib import admin
from .models import Question, Quiz, QuizAnswer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic', 'correct_answer', 'difficulty', 'ai_generated')
    list_filter = ('topic', 'difficulty', 'ai_generated')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'percentage', 'completed', 'created_at')
    list_filter = ('completed', 'difficulty')


admin.site.register(QuizAnswer)
