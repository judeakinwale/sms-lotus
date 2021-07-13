from django.shortcuts import render
from rest_framework import viewsets, permissions
from academics import models, serializers

# Create your views here.


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = models.Faculty.objects.all()
    serializer_class = serializers.FacultySerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class ProgrammeViewSet(viewsets.ModelViewSet):
    queryset = models.Programme.objects.all()
    serializer_class = serializers.ProgrammeSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class LevelViewSet(viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]
