from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.core.database import Base


class SignalStatus(str, PyEnum):
NEW = "new"
CONFIRMED = "confirmed"
EXECUTED = "executed"
FAILED = "failed"


class SignalType(str, PyEnum):
BUY = "buy"
SELL = "sell"


class Signal(Base):
__tablename__ = "signals"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
symbol: Mapped[str] = mapped_column(String(20), index=True)
type: Mapped[SignalType]
price: Mapped[float] = mapped_column(Float)
amount: Mapped[float] = mapped_column(Float, default=0.0) # в единицах базовой валюты
timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
status: Mapped[SignalStatus] = mapped_column(default=SignalStatus.NEW)


user = relationship("User", back_populates="signals")
trade = relationship("Trade", back_populates="signal", uselist=False)