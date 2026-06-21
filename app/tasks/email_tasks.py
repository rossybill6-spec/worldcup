"""
Background email tasks using Celery.
"""

from typing import Optional, List
from app.tasks.celery_app import celery_app
from app.core.email import send_email as send_email_direct


@celery_app.task(name="send_email", bind=True, max_retries=3)
def send_email_task(
    self,
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
) -> bool:
    """
    Celery task to send an email asynchronously.
    Retries up to 3 times on failure.
    """
    import asyncio
    
    try:
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(
            send_email_direct(to_email, subject, body, html_body)
        )
        return result
    except Exception as e:
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        return False


@celery_app.task(name="send_bulk_email", bind=True, max_retries=2)
def send_bulk_email_task(
    self,
    recipients: List[str],
    subject: str,
    body: str,
    html_body: Optional[str] = None,
) -> dict:
    """
    Send email to multiple recipients.
    Returns count of successful and failed sends.
    """
    success_count = 0
    fail_count = 0
    
    for email in recipients:
        try:
            result = send_email_task.delay(email, subject, body, html_body)
            success_count += 1
        except Exception:
            fail_count += 1
    
    return {"success": success_count, "failed": fail_count}
