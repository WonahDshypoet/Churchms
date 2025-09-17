from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import redirect, render

User = get_user_model()

# ================== Registration ==================
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_member=True,   # 👈 default role
            is_admin=False
        )
        return user

# Registration view
class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomLoginView(TokenObtainPairView):
    """
    Extends TokenObtainPairView to also handle form-urlencoded requests.
    """
    def post(self, request, *args, **kwargs):
        # If data comes from form instead of JSON
        if request.content_type == "application/x-www-form-urlencoded":
            email = request.POST.get("email") or request.POST.get("username")
            password = request.POST.get("password")
            request.data._mutable = True  # make data mutable
            request.data['email'] = email
            request.data['password'] = password
            request.data._mutable = False

        return super().post(request, *args, **kwargs)
    
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class EmailLoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)  # works if USERNAME_FIELD="email"
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        return render(request, self.template_name, {"error": "Invalid email or password"})
        

    