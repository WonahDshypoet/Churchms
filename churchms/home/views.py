from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from .models import Family, Member, Event, Registration, Donation, Communication, Devotional
from .serializers import (
    FamilySerializer, MemberSerializer, EventSerializer,
    RegistrationSerializer, DonationSerializer, CommunicationSerializer, DevotionalSerializer
)
from .permissions import IsAdminUserOrReadOnly, IsOwnerOrAdmin
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes
from .message_util import send_message
from .tasks import send_daily_devotional
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
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

class DevotionalTrigger(APIView):
    def post(self, request):
        send_daily_devotional.delay()  # async
        return Response({"status": "Task queued"})
    
    
class DevotionalViewSet(viewsets.ModelViewSet):
    queryset = Devotional.objects.all().order_by('-date')
    serializer_class = DevotionalSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

@api_view(['POST'])
@permission_classes([IsAdminUser])
def send_devotional_now(request):
    today = now().date()
    try:
        devotional = Devotional.objects.get(date=today)
    except Devotional.DoesNotExist:
        return Response({"error": "No devotional found for today"}, status=404)
    
    members = Member.objects.all()
    for member in members:
        message = f"Today's devotional: {devotional.message}"
        channel = getattr(member, "preferred_channel", "Email")
        send_message(member, message, channel)

    return Response({"status": f"Sent devotional to {members.count()} members"})


def dashboard(request):
    return render(request, "dashboard.html", {"user": request.user})

@login_required
def member_dashboard(request):
    devotionals = Devotional.objects.order_by('-date')[:1]
    communications = Communication.objects.order_by('-created_at')[:5]
    donations = Donation.objects.filter(member__email=request.user.email)
    total_donations = sum([d.amount for d in donations])

    return render(request, "member_dashboard.html", {
        "user": request.user,
        "devotionals": devotionals,
        "communications": communications,
        "total_donations": total_donations,
    })


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Registration successful! You can now log in.")
            return redirect("login")  # go to login page
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration.html", {"form": form})

class RoleBasedLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return "/dashboard/"
    
        
