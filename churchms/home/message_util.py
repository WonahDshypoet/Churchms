from .models import Communication

def send_message(member, message, channel="Email"):
    """
    Send message to member using the chosen channel.
    This is where you integrate Twilio, SMTP, or WhatsApp API later.
    For now, it just logs to the Communication table.
    """
    # TODO: Replace with actual email/SMS sending logic
    Communication.objects.create(
        member=member,
        message=message,
        channel=channel,
        status="Sent"
    )
    return True