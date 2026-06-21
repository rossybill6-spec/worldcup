from app.tasks.celery_app import celery_app
from app.services.push_service import PushService

@celery_app.task(name="send_push_task")
def send_push_task(device_token: str, title: str, body: str):
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(PushService.send(device_token, title, body))
