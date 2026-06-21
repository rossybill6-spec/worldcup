"""
Push notification utilities using Firebase Cloud Messaging.
"""

from typing import Optional, Dict, Any
from app.core.config import settings


async def send_push_notification(
    device_token: str,
    title: str,
    body: str,
    data: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Send a push notification to a device.
    
    Args:
        device_token: FCM device token
        title: Notification title
        body: Notification body
        data: Optional data payload
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not settings.FIREBASE_CREDENTIALS_PATH:
        print(f"⚠️  Push not configured. Would send: {title} - {body}")
        return False
    
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=device_token,
        )
        
        response = messaging.send(message)
        return response is not None
    except Exception as e:
        print(f"❌ Push notification failed: {e}")
        return False


async def send_push_to_multiple(
    device_tokens: list,
    title: str,
    body: str,
    data: Optional[Dict[str, Any]] = None,
) -> int:
    """
    Send push notification to multiple devices.
    
    Returns:
        Number of successfully sent notifications
    """
    if not settings.FIREBASE_CREDENTIALS_PATH:
        print(f"⚠️  Push not configured. Would send to {len(device_tokens)} devices")
        return 0
    
    try:
        import firebase_admin
        from firebase_admin import credentials, messaging
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=device_tokens,
        )
        
        response = messaging.send_multicast(message)
        return response.success_count
    except Exception as e:
        print(f"❌ Push notification failed: {e}")
        return 0
