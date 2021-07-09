from rest_framework import serializers
from assessment import models


class QuizSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Quiz model"""
    supervisor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Quiz
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiz-detail'}
        }


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Question model"""
    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='information:quiz-detail',
    )

    class Meta:
        model = models.Question
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assessment:question-detail'}
        }


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Answer model"""
    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='information:question-detail',
    )

    class Meta:
        model = models.Answer
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assessment:answers-detail'}
        }


class QuizTakerSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the QuizTaker model"""
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    quiz = serializers.HyperlinkedRelatedField(
        queryset=models.Quiz.objects.all(),
        view_name='information:quiz-detail',
    )

    class Meta:
        model = models.QuizTaker
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assessment:quiztaker-detail'}
        }


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Response model"""
    quiz_taker = serializers.HyperlinkedRelatedField(
        queryset=models.QuizTaker.objects.all(),
        view_name='information:quiz_taker-detail',
    )
    question = serializers.HyperlinkedRelatedField(
        queryset=models.Question.objects.all(),
        view_name='information:question-detail',
    )
    answer = serializers.HyperlinkedRelatedField(
        queryset=models.Answer.objects.all(),
        view_name='information:answer-detail',
    )

    class Meta:
        model = models.Response
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'assessment:response-detail'}
        }
