from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
def __init__(self) -> None:
self.active: Dict[int, set[WebSocket]] = {}


async def connect(self, user_id: int, websocket: WebSocket):
await websocket.accept()
self.active.setdefault(user_id, set()).add(websocket)


def disconnect(self, user_id: int, websocket: WebSocket):
if user_id in self.active and websocket in self.active[user_id]:
self.active[user_id].remove(websocket)
if not self.active[user_id]:
del self.active[user_id]


async def send_to_user(self, user_id: int, message: dict):
for ws in self.active.get(user_id, []):
await ws.send_json(message)


manager = ConnectionManager()