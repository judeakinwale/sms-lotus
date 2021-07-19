from rest_framework import serializers
from django.contrib.auth import get_user_model
from information import models
from academics import models as amodels


class InformationImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the InformationImage model"""

    information = serializers.HyperlinkedRelatedField(
        queryset=models.Information.objects.all(),
        view_name='information:information-detail',
    )

    class Meta:
        model = models.InformationImage
        fields = [
            'id',
            'url',
            'information',
            'image',
            'description',
            'timestamp'
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:informationimage-detail'}
        }


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Information model"""

    source = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), allow_null=True, required=False)
    scope = serializers.HyperlinkedRelatedField(
        queryset=models.Scope.objects.all(),
        view_name='information:scope-detail',
    )
    images = InformationImageSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Information
        lookup_field = 'id'
        fields = [
            'id',
            'url',
            'title',
            'body',
            'images',
            'source',
            'scope',
            'timestamp'
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:information-detail'},
        }


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Notice model"""

    source = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), allow_null=True, required=False)
    scope = serializers.HyperlinkedRelatedField(
        queryset=models.Scope.objects.all(),
        view_name='information:scope-detail',
    )

    class Meta:
        model = models.Notice
        fields = ['id', 'url', 'title', 'message', 'source', 'scope']
        extra_kwargs = {
            'url': {'view_name': 'information:notice-detail'}
        }


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""

    faculty = serializers.HyperlinkedRelatedField(
        queryset=amodels.Faculty.objects.all(),
        view_name='academics:faculty-detail',
        allow_null=True,
        required=False,
    )
    departmment = serializers.HyperlinkedRelatedField(
        queryset=amodels.Department.objects.all(),
        view_name='academics:departmment-detail',
        allow_null=True,
        required=False,
    )
    programme = serializers.HyperlinkedRelatedField(
        queryset=amodels.Programme.objects.all(),
        view_name='academics:programme-detail',
        allow_null=True,
        required=False,
    )
    course = serializers.HyperlinkedRelatedField(
        queryset=amodels.Course.objects.all(),
        view_name='academics:course-detail',
        allow_null=True,
        required=False,
    )
    level = serializers.HyperlinkedRelatedField(
        queryset=amodels.Level.objects.all(),
        view_name='academics:level-detail',
        allow_null=True,
        required=False,
    )
    information_set = InformationSerializer(many=True, allow_null=True, required=False)
    notice_set = NoticeSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = models.Scope
        fields = [
            'id',
            'url',
            'faculty',
            'departmment',
            'programme',
            'course',
            'level',
            'description',
            'is_general',
            'is_first_year',
            'is_final_year',
            'information_set',
            'notice_set',
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:scope-detail'}
        }
