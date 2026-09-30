from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import performance, weak_topics, recommendations


@login_required
def performance_page(request):
    context = {
        'overview': performance.student_overview(request.user),
        'topics': performance.topic_wise_performance(request.user),
        'courses': performance.course_wise_performance(request.user),
    }
    return render(request, 'student/performance.html', context)


@login_required
def recommendations_page(request):
    context = {
        'recommendations': recommendations.recommendations_for_student(request.user),
        'weak': weak_topics.strongest_and_weakest(request.user),
    }
    return render(request, 'student/recommendations.html', context)
