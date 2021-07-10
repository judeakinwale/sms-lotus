from rest_framework import serializers
from assessment import models


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Quiz model"""
    supervisor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Quiz
        fields = [
            'id',
            'url',
            'supervisor',
            'name',
            'question_count',
            'description',
            'is_active',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiz-detail'}
        }


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Question model"""
    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='assessment:quiz-detail',
    )

    class Meta:
        model = models.Question
        fields = [
            'id',
            'url',
            'quiz',
            'label',
            'order',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:question-detail'}
        }


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Answer model"""
    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='assessment:question-detail',
    )

    class Meta:
        model = models.Answer
        fields = [
            'id',
            'url',
            'question',
            'text',
            'is_correct',
        ]
        # read_only_fields = ['id']
        extra_kwargs = {
            'url': {'view_name': 'assessment:answer-detail'}
        }


class QuizTakerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the QuizTaker model"""
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='assessment:quiz-detail',
    )

    class Meta:
        model = models.QuizTaker
        fields = [
            'id',
            'url',
            'student',
            'quiz',
            'correct_answer',
            'completed',
            'timestamp',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiztaker-detail'}
        }


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Response model"""
    quiz_taker = serializers.HyperlinkedRelatedField(
        queryset=models.QuizTaker.objects.all(),
        view_name='assessment:quiz_taker-detail',
    )
    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='assessment:question-detail',
    )
    answer = serializers.HyperlinkedRelatedField(
        queryset=models.Answer.objects.all(),
        view_name='assessment:answer-detail',
    )

    class Meta:
        model = models.Response
        fields = [
            'id',
            'url',
            'quiz_taker',
            'question',
            'answer',
        ]
        extra_kwargs = {
            'url': {'view_name': 'assessment:response-detail'}
        }
