from rest_framework import serializers
from .models import Family, Member, Event, Registration, Donation, Communication, CustomUser, Devotional
from django.contrib.auth import get_user_model  


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_member', 'is_admin')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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
    member_name = serializers.StringRelatedField(source='member', read_only=True)
    event_name = serializers.StringRelatedField(source='event', read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'


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