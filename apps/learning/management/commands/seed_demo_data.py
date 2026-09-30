from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.learning.models import Course, Topic
from apps.quizzes.models import Question

User = get_user_model()

DEMO_COURSES = {
    'Mathematics': ('∑', ['Algebra', 'Geometry', 'Trigonometry']),
    'Physics': ('⚛️', ['Motion', 'Energy', 'Electricity']),
}


class Command(BaseCommand):
    help = 'Seeds demo accounts and a starter set of courses/topics for the demo student.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'admin@cerebrox.local', 'AdminPass123',
                role=User.Role.ADMIN, study_level=User.StudyLevel.GRADUATE,
            )
            self.stdout.write(self.style.SUCCESS('Created admin / AdminPass123'))

        student, created = User.objects.get_or_create(
            username='student',
            defaults=dict(
                email='student@cerebrox.local', first_name='Demo', last_name='Student',
                role=User.Role.STUDENT, study_level=User.StudyLevel.UNDERGRADUATE,
            ),
        )
        if created:
            student.set_password('StudentPass123')
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student / StudentPass123'))

        # Courses/topics are per-student — these are just starter examples for the
        # demo account, not global/shared content.
        for course_name, (icon, topics) in DEMO_COURSES.items():
            course, _ = Course.objects.get_or_create(student=student, name=course_name, defaults={'icon': icon})
            for topic_name in topics:
                topic, created_topic = Topic.objects.get_or_create(
                    course=course, name=topic_name,
                    defaults={'description': f'Core concepts of {topic_name}.'},
                )
                if created_topic:
                    Question.objects.create(
                        topic=topic,
                        question=f'Which of these is most closely associated with {topic_name}?',
                        option_a=f'{topic_name} fundamentals', option_b='Unrelated concept B',
                        option_c='Unrelated concept C', option_d='Unrelated concept D',
                        correct_answer='A', explanation=f'{topic_name} fundamentals is the core idea here.',
                        difficulty='Easy',
                    )
        self.stdout.write(self.style.SUCCESS('Demo data seeded.'))
