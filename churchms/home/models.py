from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# ======= FAMILY & MEMBER MODELS =======
class Family(models.Model):
    family_name = models.CharField(max_length=100)

    def __str__(self):
        return self.family_name
    
    
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    membership_status = models.CharField(max_length=50)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ======= EVENT MANAGEMENT =======
class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Registered')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member} -> {self.event}"


# ======= FINANCIAL TRACKING =======
class Donation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    purpose = models.CharField(max_length=100, default='Tithe/Offering')

    def __str__(self):
        return f"{self.amount} from {self.member or 'Anonymous'}"


# ======= COMMUNICATION LOG =======
class Communication(models.Model):
    CHANNEL_CHOICES = [
        ('SMS', 'SMS'),
        ('EMAIL', 'Email'),
    ]
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, default='Sent')

    def __str__(self):
        return f"{self.channel} to {self.member}"

class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    