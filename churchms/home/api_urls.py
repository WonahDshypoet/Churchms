from django.urls import path, include
from rest_framework.routers import DefaultRouter, TokenObtainPairView, TokenRefreshView
from .views import (
    FamilyViewSet, MemberViewSet, EventViewSet,
    RegistrationViewSet, DonationViewSet, CommunicationViewSet
)
from .auth_views import RegisterView


router = DefaultRouter()
router.register(r'families', FamilyViewSet)
router.register(r'members', MemberViewSet)
router.register(r'events', EventViewSet)
router.register(r'registrations', RegistrationViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'communications', CommunicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]