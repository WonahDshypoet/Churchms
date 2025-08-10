from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Family, Member, Event, Registration, Donation, Communication
from .serializers import (
    FamilySerializer, MemberSerializer, EventSerializer,
    RegistrationSerializer, DonationSerializer, CommunicationSerializer
)
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrAdmin
# Create your views here.


# Family ViewSet
class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer
    
    
# Member ViewSet
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    

# Event ViewSet
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    
    
# Registration ViewSet
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


# Donation ViewSet
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            user = self.request.user
            if user.is_admin:
                return Donation.objects.all()
            # Members only see their own donations
            return Donation.objects.filter(member__email=user.email)

# Communication ViewSet
class CommunicationViewSet(viewsets.ModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer

