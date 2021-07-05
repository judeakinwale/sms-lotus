from django.shortcuts import render
from rest_framework import generics, viewsets, authentication, permissions
from rest_framework.serializers import Serializer
from information import models, serializers

# Create your views here.


class InformationViewSet(viewsets.ModelViewSet):
    queryset = models.Information.objects.all()
    serializer_class = serializers.InformationSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = models.Notice.objects.all()
    serializer_class = serializers.NoticeSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]

    def perform_create(self, serializer):
        return serializer.save(source=self.request.user)


class InformationImageViewSet(viewsets.ModelViewSet):
    queryset = models.InformationImage.objects.all()
    serializer_class = serializers.InformationImageSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = models.Scope.objects.all()
    serializer_class = serializers.ScopeSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]
