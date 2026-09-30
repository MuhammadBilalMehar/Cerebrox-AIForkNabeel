from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(TestCase):
    def test_register_creates_student(self):
        c = Client()
        resp = c.post('/accounts/register/', {
            'username': 'newstudent', 'first_name': 'New', 'last_name': 'Student',
            'email': 'new@student.com', 'study_level': User.StudyLevel.UNDERGRADUATE,
            'password1': 'StrongPass123', 'password2': 'StrongPass123',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/learning/courses/', resp.url)  # new registrations land on course setup
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.study_level, User.StudyLevel.UNDERGRADUATE)

    def test_login_with_wrong_password_fails(self):
        User.objects.create_user('bob', 'bob@x.com', 'CorrectPass123')
        c = Client()
        resp = c.post('/accounts/login/', {'username': 'bob', 'password': 'WrongPass'})
        self.assertEqual(resp.status_code, 200)  # re-renders login form with error
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_dashboard_requires_login(self):
        c = Client()
        resp = c.get('/dashboard/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)
