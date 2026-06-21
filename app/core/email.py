"""
Email sending utilities using SMTP.
Supports both sync and async sending with Jinja2 templates.
"""

from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from jinja2 import Environment, BaseLoader

from app.core.config import settings


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> bool:
    """
    Send an email asynchronously.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text body
        html_body: Optional HTML body
        cc: Optional CC recipients
        bcc: Optional BCC recipients
    
    Returns:
        True if sent successfully, False otherwise
    """
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"⚠️  Email not configured. Would send to {to_email}: {subject}")
        return False
    
    try:
        message = MIMEMultipart("alternative")
        message["From"] = settings.SMTP_FROM
        message["To"] = to_email
        message["Subject"] = subject
        
        if cc:
            message["Cc"] = ", ".join(cc)
        if bcc:
            message["Bcc"] = ", ".join(bcc)
        
        message.attach(MIMEText(body, "plain"))
        if html_body:
            message.attach(MIMEText(html_body, "html"))
        
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False


def render_template(template_string: str, context: dict) -> str:
    """Render a Jinja2 template string with context."""
    env = Environment(loader=BaseLoader())
    template = env.from_string(template_string)
    return template.render(**context)
