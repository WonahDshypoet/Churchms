from celery import shared_task
from django.utils.timezone import now
from .models import Devotional, Member
from .message_util import send_message

@shared_task
def send_daily_devotional():
    today = now().date()
    try:
        devotional = Devotional.objects.get(date=today)
    except Devotional.DoesNotExist:
        return "No devotional for today"
    
    members = Member.objects.all()
    for member in members:
        message = f"Today's devotional: {devotional.message}"
        # Use member.preferred_channel if available
        channel = getattr(member, "preferred_channel", "Email")
        send_message(member, message, channel)
    
    return f"Sent devotional to {members.count()} members"