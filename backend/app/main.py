from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, users, signals, trades
from app.websocket.manager import manager
from app.core.database import engine
from app.models import Base


app = FastAPI(title=settings.APP_NAME)


app.add_middleware(
CORSMiddleware,
allow_origins=settings.CORS_ORIGINS,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


# Создаем таблицы при старте (для dev). В проде используйте Alembic миграции
Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(signals.router, prefix=settings.API_V1_PREFIX)
app.include_router(trades.router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
def health():
return {"ok": True}


@app.websocket("/ws/{user_id}")
async def ws_endpoint(websocket: WebSocket, user_id: int):
await manager.connect(user_id, websocket)
try:
while True:
await websocket.receive_text() # ping/pong
except WebSocketDisconnect:
manager.disconnect(user_id, websocket)