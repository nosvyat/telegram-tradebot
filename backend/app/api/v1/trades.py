from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.trade import Trade
from .users import current_user


router = APIRouter(prefix="/trades", tags=["trades"])


@router.get("/")
def list_trades(db: Session = Depends(get_db), user = Depends(current_user)):
return db.query(Trade).filter(Trade.user_id == user.id).order_by(Trade.timestamp.desc()).all()


@router.get("/stats")
def stats(db: Session = Depends(get_db), user = Depends(current_user)):
total = db.query(func.count(Trade.id)).filter(Trade.user_id == user.id).scalar() or 0
pnl = db.query(func.coalesce(func.sum(Trade.pnl), 0.0)).filter(Trade.user_id == user.id).scalar() or 0.0
return {"trades": total, "pnl": pnl}