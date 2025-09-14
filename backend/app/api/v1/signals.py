from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.signal import Signal, SignalStatus
from app.models.user import User
from app.schemas.signal import SignalIn, SignalOut
from app.services.trading import TradingService
from .users import current_user


router = APIRouter(prefix="/signals", tags=["signals"])


@router.post("/webhook")
def tradingview_webhook(secret: str, payload: SignalIn, db: Session = Depends(get_db)):
if secret != settings.TV_WEBHOOK_SECRET:
raise HTTPException(403, "Forbidden")
# ⚠️ Здесь нужен mapping user_id ↔️ сигнал (из вашего источника)
# Для примера кладем на user_id=1
user = db.query(User).get(1)
if not user:
raise HTTPException(404, "User not found")
sig = Signal(user_id=user.id, symbol=payload.symbol, type=payload.type, price=payload.price, amount=payload.amount)
db.add(sig)
db.commit()
db.refresh(sig)


if user.auto_trading:
TradingService.execute_signal(db, user, sig)


return {"id": sig.id, "status": sig.status}


@router.get("/", response_model=list[SignalOut])
def list_signals(db: Session = Depends(get_db), user: User = Depends(current_user)):
return db.query(Signal).filter(Signal.user_id == user.id).order_by(Signal.timestamp.desc()).all()


@router.post("/{signal_id}/confirm")
def confirm_signal(signal_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
sig = db.query(Signal).filter(Signal.id == signal_id, Signal.user_id == user.id).first()
if not sig:
raise HTTPException(404, "Signal not found")
trade = TradingService.execute_signal(db, user, sig)
return {"trade_id": trade.id, "signal_status": sig.status}