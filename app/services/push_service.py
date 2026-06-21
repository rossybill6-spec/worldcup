class PushService:
    @staticmethod
    async def send(device_token: str, title: str, body: str) -> bool:
        print(f"[PUSH] To: {device_token[:10]}... | {title}: {body}")
        return True
