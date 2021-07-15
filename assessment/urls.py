from django.urls import path, include
from rest_framework.routers import DefaultRouter
from assessment import views

app_name = 'assessment'

router = DefaultRouter()
router.register('quiz', views.QuizViewSet)
router.register('question', views.QuestionViewSet)
router.register('answer', views.AnswerViewSet)
router.register('quizTaker', views.QuizTakerViewSet)
router.register('response', views.ResponseViewSet)
router.register('grade', views.GradeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
