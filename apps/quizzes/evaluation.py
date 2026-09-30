"""Pure backend scoring logic — no AI involved (per FYP scope §18)."""
from django.db import transaction


@transaction.atomic
def submit_quiz(quiz, answers_by_question_id: dict):
    """answers_by_question_id: {question_id(str/int): 'A'|'B'|'C'|'D'}"""
    correct_count = 0
    quiz_answers = quiz.answers.select_related('question').all()
    for qa in quiz_answers:
        selected = answers_by_question_id.get(str(qa.question_id), '')
        qa.selected_answer = selected
        qa.correct = bool(selected) and selected.upper() == qa.question.correct_answer
        if qa.correct:
            correct_count += 1
        qa.save(update_fields=['selected_answer', 'correct'])

    quiz.score = correct_count
    quiz.percentage = round((correct_count / quiz.total_questions) * 100, 1) if quiz.total_questions else 0
    quiz.completed = True
    quiz.save(update_fields=['score', 'percentage', 'completed'])

    _award_xp(quiz)
    return quiz


def _award_xp(quiz):
    from django.conf import settings
    rules = settings.XP_RULES
    xp = rules['QUIZ_COMPLETED']
    if quiz.percentage > 90:
        xp += rules['SCORE_ABOVE_90']
    elif quiz.percentage > 80:
        xp += rules['SCORE_ABOVE_80']
    student = quiz.student
    student.xp_points = (student.xp_points or 0) + xp
    student.save(update_fields=['xp_points'])
