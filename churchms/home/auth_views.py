from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth import get_user_model  
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers


# Serializer for registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        User = get_user_model()
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user

# Registration view
class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# Login view is handled by SimpleJWT (TokenObtainPairView)

class CustomLoginView(TokenObtainPairView):
    """
    Extends TokenObtainPairView to also handle form-urlencoded requests.
    """
    def post(self, request, *args, **kwargs):
        # If data comes from form instead of JSON
        if request.content_type == "application/x-www-form-urlencoded":
            username = request.POST.get("username")
            password = request.POST.get("password")
            request.data._mutable = True  # make data mutable
            request.data['username'] = username
            request.data['password'] = password
            request.data._mutable = False

        return super().post(request, *args, **kwargs)