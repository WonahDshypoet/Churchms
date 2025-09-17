from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Devotional, Member
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    FamilyViewSet, MemberViewSet, EventViewSet,
    RegistrationViewSet, DonationViewSet, CommunicationViewSet, DevotionalViewSet, send_devotional_now
)
from .auth_views import RegisterView
from django.utils.timezone import now
from .message_util import send_message
from .auth_views import CurrentUserView


router = DefaultRouter()
router.register(r'families', FamilyViewSet)
router.register(r'members', MemberViewSet)
router.register(r'events', EventViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'communications', CommunicationViewSet)
router.register(r'devotionals', DevotionalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('devotionals/send-now/', send_devotional_now, name='send_devotional_now'),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", CurrentUserView.as_view(), name="auth_me"),
]