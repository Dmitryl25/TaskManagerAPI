from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.connection_manager import manager
from app.core.security import decode_token


router = APIRouter()

@router.websocket("/ws/notifications")
async def notification(websocket: WebSocket):
    token = websocket.query_params.get("token")
    decoded_token = decode_token(token)
    if not decoded_token:
        await websocket.close()
        return
    await websocket.accept()
    manager.connect(decoded_token["sub"], websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(decoded_token["sub"], websocket)

