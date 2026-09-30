from .weak_topics import classify
from apps.ai_engine.recommendation_generator import phrase_recommendation

RULES = {
    'Weak': 'Review the fundamentals of {topic} and attempt another practice quiz before moving on.',
    'Needs Practice': 'You are close on {topic} — a bit more practice will get you to a strong score.',
    'Strong': "Great work on {topic} — you're ready to progress to the next topic.",
}


def recommendation_for_topic(topic_name: str, score_percent: float, use_ai: bool = True) -> dict:
    status = classify(score_percent)
    fallback_text = RULES[status].format(topic=topic_name)
    message = fallback_text
    if use_ai:
        message = phrase_recommendation(topic_name, score_percent, status, fallback_text)
    return {'topic': topic_name, 'score': score_percent, 'status': status, 'message': message}


def recommendations_for_student(student, use_ai: bool = True):
    from .weak_topics import topic_wise_performance
    return [
        recommendation_for_topic(row['topic__name'], row['avg_score'], use_ai)
        for row in topic_wise_performance(student)
    ]
