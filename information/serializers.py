from rest_framework import fields, serializers
from information import models


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Information model"""
    source = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.Information
        fields = ['url', 'title', 'body', 'source', 'scope', 'timestamp']


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Notice model"""
    source = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.Notice
        fields = ['url', 'title', 'message', 'source', 'scope']


class InformationImageSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the InformationImage model"""
    class Meta:
        model = models.InformationImage
        fields = ['url', 'information', 'image', 'description', 'timestamp']


class ScopeSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the Scope model"""
    class Meta:
        model = models.Scope
        fields = ['url', 'is_general', 'is_first_year', 'is_final_year']
