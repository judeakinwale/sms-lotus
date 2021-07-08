from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Quiz(models.Model):

    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    question_count = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        get_latest_by = "timestamp"
        ordering = ["-timestamp"]
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.name


class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=250)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.label


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(False)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.text


class QuizTaker(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    correct_answer = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("QuizTaker")
        verbose_name_plural = _("QuizTakers")

    def __str__(self):
        return self.quiz


class Response(models.Model):

    quiztaker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        return self.question.label
