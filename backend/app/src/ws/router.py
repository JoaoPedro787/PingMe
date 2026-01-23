from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Annotated
from auth.dependencies import validate_user_token, get_current_user

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

# Criar outra dependencia, que verifica se o user está no chat da rota. Ex: chat 1 tem user 1 e user 2, user 3 não pode entrar


@router.websocket("/chat/{chat_id}", dependencies=[Depends(validate_user_token)])
async def websocket_endpoint(
    chat_id: int, websocket: WebSocket, user_id=Depends(get_current_user)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")
