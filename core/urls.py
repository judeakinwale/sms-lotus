from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as JWTViews
from core import views


app_name = 'core'

router = DefaultRouter()
router.register('user', views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", JWTViews.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify", JWTViews.TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh", JWTViews.TokenRefreshView.as_view(), name="token_refresh"),
]
