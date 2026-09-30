"""Turns AI-generated question data into real Question rows and starts a
Quiz + its QuizAnswer placeholders, for one or more of the student's own Topics."""
from django.db import transaction
from .models import Question, Quiz, QuizAnswer
from apps.ai_engine.mcq_generator import generate_questions


@transaction.atomic
def create_ai_quiz(student, topic, difficulty, num_questions, extra_topics=None):
    topics = list(extra_topics or [])
    if topic not in topics:
        topics.insert(0, topic)
    study_level = student.effective_study_level

    question_records = []
    for selected_topic in topics:
        raw_questions = generate_questions(
            selected_topic.course.name, selected_topic.name, study_level, difficulty, num_questions,
        )
        for item in raw_questions:
            q = Question.objects.create(
                topic=selected_topic,
                question=item['question'],
                option_a=item['option_a'], option_b=item['option_b'],
                option_c=item['option_c'], option_d=item['option_d'],
                correct_answer=item['correct_answer'].upper()[:1],
                explanation=item.get('explanation', ''),
                difficulty=difficulty,
                ai_generated=True,
            )
            question_records.append(q)

    quiz = Quiz.objects.create(
        student=student, topic=topic, difficulty=difficulty, study_level=study_level,
        total_questions=len(question_records), duration_seconds=max(60, len(question_records) * 60),
    )
    if topics:
        quiz.topics.set(topics)
    QuizAnswer.objects.bulk_create([QuizAnswer(quiz=quiz, question=q) for q in question_records])
    return quiz
