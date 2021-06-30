from django.shortcuts import render
from rest_framework import generics, viewsets, authentication, permissions
from information import models, serializers

# Create your views here.


class InformationViewSet(viewsets.ModelViewSet):
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly, ]


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly, ]


class InformationImageViewSet(viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly, ]


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly, ]
