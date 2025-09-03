from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
# Create your models here.


# ======= FAMILY 
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

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save first
        success = False  

        if self.channel == "EMAIL" and self.member and self.member.email:
            try:
                send_mail(
                    subject="Church Message",
                    message=self.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.member.email],
                )
                success = True
            except Exception as e:
                print("Email error:", e)

        elif self.channel == "SMS" and self.member and self.member.phone:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client.messages.create(
                    body=self.message,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=self.member.phone,
                )
                success = True
            except Exception as e:
                print("SMS error:", e)

        self.status = "Sent" if success else "Failed"
        super().save(update_fields=["status"])


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_member = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username still required by AbstractUser

    def __str__(self):
        return self.email
    