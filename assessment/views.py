from django.shortcuts import render
from rest_framework import viewsets, permissions
from assessment import models, serializers

# Create your views here.


class QuizViewSet(viewsets.ModelViewSet):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class QuizTakerViewSet(viewsets.ModelViewSet):
    queryset = models.QuizTaker.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = models.Response.objects.all()
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]
