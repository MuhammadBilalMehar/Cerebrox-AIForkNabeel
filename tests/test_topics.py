from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.learning.models import Course, Topic

User = get_user_model()


class TopicTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user('stud2', 's2@s.com', 'StudPass123', role=User.Role.STUDENT)
        self.other_student = User.objects.create_user('stud2b', 's2b@s.com', 'StudPass123', role=User.Role.STUDENT)
        self.course = Course.objects.create(student=self.student, name='Mathematics', icon='∑')
        self.topic = Topic.objects.create(course=self.course, name='Algebra', description='desc')

    def test_topic_list_for_course(self):
        c = Client(); c.login(username='stud2', password='StudPass123')
        resp = c.get(f'/learning/courses/{self.course.id}/topics/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Algebra')

    def test_topic_detail_page(self):
        c = Client(); c.login(username='stud2', password='StudPass123')
        resp = c.get(f'/learning/topics/{self.topic.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_other_student_cannot_access_topic(self):
        c = Client(); c.login(username='stud2b', password='StudPass123')
        resp = c.get(f'/learning/topics/{self.topic.id}/')
        self.assertEqual(resp.status_code, 404)
