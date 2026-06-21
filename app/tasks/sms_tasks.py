from app.tasks.celery_app import celery_app
from app.core.sms import send_sms

@celery_app.task(name="send_sms_task")
def send_sms_task(to_phone: str, message: str):
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(send_sms(to_phone, message))
