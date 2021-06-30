from django.urls import path, include
from rest_framework.routers import DefaultRouter
from information import views


app_name = 'information'

router = DefaultRouter()
router.register('information', views.InformationViewSet)
router.register('image', views.InformationImageViewSet)
router.register('notice', views.NoticeViewSet)
router.register('scope', views.ScopeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
