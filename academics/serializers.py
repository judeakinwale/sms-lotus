from django.db.models import fields
from rest_framework import serializers
from academics import models


class FacultySerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Faculty model"""

    class Meta:
        model = models.Faculty
        fields = [
            'id',
            'url',
            'name',
            'code',
            'description',
            'dean',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:faculty-detail'}
        }


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Department model"""

    faculty = serializers.HyperlinkedRelatedField(
        queryset=models.Faculty.objects.all(),
        view_name='academics:faculty-detail',
    )

    class Meta:
        model = models.Department
        fields = [
            'id',
            'url',
            'faculty',
            'name',
            'code',
            'description',
            'head',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:department-detail'}
        }


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Programme model"""

    department = serializers.HyperlinkedRelatedField(
        queryset=models.Department.objects.all(),
        view_name='academics:department-detail',
    )
    max_level = serializers.HyperlinkedRelatedField(
        queryset=models.Level.objects.all(),
        view_name='academics:level-detail',
    )
    # max_level = serializers.StringRelatedField()

    class Meta:
        model = models.Programme
        fields = [
            'id',
            'url',
            'department',
            'name',
            'code',
            'max_level',
            'description',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:programme-detail'}
        }


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Course model"""

    programme = serializers.HyperlinkedRelatedField(
        queryset=models.Programme.objects.all(),
        view_name='academics:programme-detail',
    )

    class Meta:
        model = models.Course
        fields = [
            'id',
            'url',
            'programme',
            'name',
            'code',
            'description',
            'coordinator',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:course-detail'}
        }


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Level model"""

    class Meta:
        model = models.Level
        fields = [
            'id',
            'url',
            'code',
        ]
        extra_kwargs = {
            'url': {'view_name': 'academics:level-detail'}
        }
