from django.conf import settings
from .performance import topic_wise_performance


def classify(score_percent: float) -> str:
    thresholds = settings.WEAK_TOPIC_THRESHOLDS
    if score_percent >= thresholds['STRONG']:
        return 'Strong'
    if score_percent >= thresholds['NEEDS_PRACTICE']:
        return 'Needs Practice'
    return 'Weak'


def weak_topics_for(student):
    """Simple threshold-based approach (FYP scope Module 8) — deliberately
    avoids a machine-learning adaptive-learning engine."""
    results = []
    for row in topic_wise_performance(student):
        status = classify(row['avg_score'])
        results.append({**row, 'status': status})
    return results


def strongest_and_weakest(student):
    topics = weak_topics_for(student)
    weak = [t for t in topics if t['status'] == 'Weak']
    strong = [t for t in topics if t['status'] == 'Strong']
    return {'weak': weak, 'strong': strong, 'all': topics}
