from django.urls import path, include
from rest_framework.routers import DefaultRouter
from academics import views

app_name = 'academics'

router = DefaultRouter()
router.register('faculty', views.FacultyViewSet)
router.register('department', views.DepartmentViewSet)
router.register('programme', views.ProgrammeViewSet)
router.register('course', views.CourseViewSet)
router.register('level', views.LevelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]