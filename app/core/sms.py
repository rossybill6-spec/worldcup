"""
SMS sending utilities using Twilio.
"""

from app.core.config import settings


async def send_sms(to_phone: str, message: str) -> bool:
    """
    Send an SMS message using Twilio.
    
    Args:
        to_phone: Recipient phone number (E.164 format: +1234567890)
        message: SMS body text
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print(f"⚠️  SMS not configured. Would send to {to_phone}: {message}")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        return msg.sid is not None
    except Exception as e:
        print(f"❌ SMS send failed: {e}")
        return False
