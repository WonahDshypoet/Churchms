from rest_framework import serializers
from .models import Family, Member, Event, Registration, Donation, Communication, CustomUser, Devotional
from django.contrib.auth import get_user_model  


User = get_user_model()


# ==== Family Serializer ====
class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = '__all__'


# ==== Member Serializer ====
class MemberSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.family_name', read_only=True)

    class Meta:
        model = Member
        fields = '__all__'


# ==== Event Serializer ====
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        

# ==== Registration Serializer ====
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ("username","email", "password")

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])  # 🔒 hash password
        user.save()
        return user


# ==== Donation Serializer ====
class DonationSerializer(serializers.ModelSerializer):
    member_name = serializers.StringRelatedField(source='member', read_only=True)

    class Meta:
        model = Donation
        fields = '__all__'


# ==== Communication Serializer ====
class CommunicationSerializer(serializers.ModelSerializer):
    member_name = serializers.StringRelatedField(source='member', read_only=True)

    class Meta:
        model = Communication
        fields = '__all__'
        

# ==== Devotional Serializer ====     
class DevotionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devotional
        fields = "__all__"
        
        
# ==== User Serializer ====
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "is_admin", "is_member"]