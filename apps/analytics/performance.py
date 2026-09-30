"""
Performance is calculated dynamically from Quiz/QuizAnswer history rather
than stored in its own table, per the scope doc's simplification note in
§21 ("Performance can either be stored separately or calculated from quiz
attempts... simpler to calculate dynamically").
"""
from django.db.models import Avg, Max, Min, Count
from apps.quizzes.models import Quiz


def student_overview(student):
    qs = Quiz.objects.filter(student=student, completed=True)
    agg = qs.aggregate(
        total=Count('id'), avg=Avg('percentage'), best=Max('percentage'), worst=Min('percentage'),
    )
    return {
        'total_quizzes': agg['total'] or 0,
        'average_score': round(agg['avg'] or 0, 1),
        'highest_score': round(agg['best'] or 0, 1),
        'lowest_score': round(agg['worst'] or 0, 1),
        'recent_quizzes': qs.select_related('topic', 'topic__course')[:5],
    }


def topic_wise_performance(student):
    """Average percentage per topic, most recent attempts weighted equally."""
    qs = (
        Quiz.objects.filter(student=student, completed=True)
        .values('topic__id', 'topic__name', 'topic__course__name')
        .annotate(avg_score=Avg('percentage'), attempts=Count('id'))
        .order_by('-avg_score')
    )
    return list(qs)


def course_wise_performance(student):
    qs = (
        Quiz.objects.filter(student=student, completed=True)
        .values('topic__course__id', 'topic__course__name')
        .annotate(avg_score=Avg('percentage'), attempts=Count('id'))
        .order_by('-avg_score')
    )
    return list(qs)
