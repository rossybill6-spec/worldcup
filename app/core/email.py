"""
Email sending utilities using SMTP.
"""

from typing import List, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
) -> bool:
    """Send an email asynchronously. Returns True if sent successfully."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning(f"Email not configured. Would send to {to_email}: {subject}")
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
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Email send failed to {to_email}: {e}")
        return False


def render_template(template_string: str, context: dict) -> str:
    """Render a Jinja2 template string with context."""
    from jinja2 import Environment, BaseLoader
    env = Environment(loader=BaseLoader())
    template = env.from_string(template_string)
    return template.render(**context)
