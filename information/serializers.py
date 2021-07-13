from rest_framework import serializers
from information import models


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Information model"""
    source = serializers.PrimaryKeyRelatedField(read_only=True)
    scope = serializers.HyperlinkedRelatedField(
        queryset=models.Scope.objects.all(),
        view_name='information:scope-detail',
    )

    class Meta:
        model = models.Information
        lookup_field = 'id'
        fields = [
            'id',
            'url',
            'title',
            'body',
            'source',
            'scope',
            'timestamp'
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:information-detail'},
        }


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Notice model"""
    source = serializers.PrimaryKeyRelatedField(read_only=True)
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


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""
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
        ]
        extra_kwargs = {
            'url': {'view_name': 'information:scope-detail'}
        }
