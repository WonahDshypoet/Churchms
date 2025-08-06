from rest_framework import serializers
from .models import Family, Member, Event, Registration, Donation, Communication, CustomUser


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