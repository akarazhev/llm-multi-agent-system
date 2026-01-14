from typing import Dict, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.auth.keycloak import decode_token


router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, workflow_id: str) -> None:
        await websocket.accept()
        if workflow_id not in self.active_connections:
            self.active_connections[workflow_id] = set()
        self.active_connections[workflow_id].add(websocket)

    def disconnect(self, websocket: WebSocket, workflow_id: str) -> None:
        if workflow_id in self.active_connections:
            self.active_connections[workflow_id].discard(websocket)

    async def broadcast(self, workflow_id: str, message: dict) -> None:
        if workflow_id not in self.active_connections:
            return
        disconnected: Set[WebSocket] = set()
        for connection in self.active_connections[workflow_id]:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        for connection in disconnected:
            self.active_connections[workflow_id].discard(connection)


manager = ConnectionManager()


@router.websocket("/workflows/{workflow_id}")
async def workflow_ws(websocket: WebSocket, workflow_id: str) -> None:
    token = websocket.query_params.get("token")
    try:
        if token:
            await decode_token(token)
    except Exception:
        await websocket.close(code=1008)
        return
    await manager.connect(websocket, workflow_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, workflow_id)
