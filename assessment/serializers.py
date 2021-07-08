from rest_framework import serializers
from assessment import models


class QuizSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Quiz
        fields = '__all__'


class QuestionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Question
        fields = '__all__'


class AnswerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Answer
        fields = '__all__'


class QuizTakerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.QuizTaker
        fields = '__all__'


class ResponseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Response
        fields = '__all__'
