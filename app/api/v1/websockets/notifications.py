from fastapi import APIRouter, WebSocket, WebSocketDisconnect
router = APIRouter()

@router.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Notification: {data}")
    except WebSocketDisconnect:
        pass
