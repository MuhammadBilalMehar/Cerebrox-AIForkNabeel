from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    CerebroX custom user.
    role drives access control across the whole project:
    - 'student' can browse subjects/topics, generate notes/quizzes, see their own analytics.
    - 'admin' can manage subjects/topics/questions and view students (apps.accounts.admin_urls).
    Django's own is_staff/is_superuser are kept separate for the built-in /django-admin/.
    """

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'

    class StudyLevel(models.TextChoices):
        MATRIC = 'matric', 'Matric'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        UNDERGRADUATE = 'undergraduate', 'Undergraduate'
        GRADUATE = 'graduate', 'Graduate'
        OTHER = 'other', 'Other'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True, null=True)
    xp_points = models.PositiveIntegerField(default=0)

    # Study Level drives AI note/quiz generation (course + topic + study level + difficulty).
    study_level = models.CharField(max_length=15, choices=StudyLevel.choices, default=StudyLevel.UNDERGRADUATE)
    study_level_custom = models.CharField(
        max_length=60, blank=True,
        help_text="Used when study_level = 'Other' (e.g. 'Diploma', 'Bootcamp').",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def effective_study_level(self) -> str:
        """The human-readable study level to feed into AI prompts / show in the UI."""
        if self.study_level == self.StudyLevel.OTHER and self.study_level_custom:
            return self.study_level_custom
        return self.get_study_level_display()

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return self.get_full_name() or self.username
