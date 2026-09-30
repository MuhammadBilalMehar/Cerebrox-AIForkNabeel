from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

from .models import Quiz
from .serializers import QuizSerializer, QuestionSerializer
from .services import create_ai_quiz
from .evaluation import submit_quiz
from apps.learning.models import Topic


class GenerateQuizAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        topic = Topic.objects.select_related('course').get(pk=request.data['topic_id'], course__student=request.user)
        difficulty = request.data.get('difficulty', 'Medium')
        num_questions = int(request.data.get('num_questions', 10))
        quiz = create_ai_quiz(request.user, topic, difficulty, num_questions)
        questions = [QuestionSerializer(a.question).data for a in quiz.answers.select_related('question').all()]
        return Response({'quiz': QuizSerializer(quiz).data, 'questions': questions})


class SubmitQuizAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        quiz = Quiz.objects.get(pk=pk, student=request.user)
        submit_quiz(quiz, request.data.get('answers', {}))
        return Response(QuizSerializer(quiz).data)


class QuizDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(student=self.request.user)
