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

