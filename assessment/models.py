from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from academics.models import Course

# Create your models here.


class Quiz(models.Model):
    """Model definition for Quiz."""

    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(default=10)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Quiz."""

        get_latest_by = "timestamp"
        ordering = ["-timestamp"]
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        """String representation of Quiz."""
        return self.name


class Question(models.Model):
    """Model definition for Question."""

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    label = models.CharField(max_length=250)
    order = models.IntegerField(default=0)

    class Meta:
        """Meta definition for Question."""

        ordering = ['order']
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        """String representation of Question."""
        return self.label


class Answer(models.Model):
    """Model definition for Answer."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Answer."""

        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        """String representation of Answer."""
        return self.text


class QuizTaker(models.Model):
    """Model definition for QuizTaker."""

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ManyToManyField(Quiz, blank=True)
    grade = models.ManyToManyField("Grade", blank=True)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for QuizTaker."""

        verbose_name = _("QuizTaker")
        verbose_name_plural = _("QuizTakers")

    def __str__(self):
        """String representation of QuizTaker."""
        return f"{self.student}"


class Response(models.Model):
    """Model definition for Response."""

    quiz_taker = models.ForeignKey(QuizTaker, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """Meta definition for Response."""
        
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")

    def __str__(self):
        """String representation of Response."""
        return self.question.label


class Grade(models.Model):
    """Model definition for Grade."""

    # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField(default=10)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Grade."""

        verbose_name = _('Grade')
        verbose_name_plural = _('Grades')

    def __str__(self):
        """String representation of Grade."""
        return f"{self.score} of {self.max_score}"

    def get_value(self):
        if self.score/self.max_score >= 0.5:
            return 'Pass'
        else:
            return 'Fail'

