from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (
    UserViewSet,
    PasswordResetViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'password-reset', PasswordResetViewSet, basename='password-reset')

urlpatterns = [
    path('', include(router.urls)),
]
