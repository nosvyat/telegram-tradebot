from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base


class Trade(Base):
__tablename__ = "trades"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
signal_id: Mapped[int] = mapped_column(ForeignKey("signals.id"))


pnl: Mapped[float] = mapped_column(Float, default=0.0)
amount: Mapped[float] = mapped_column(Float)
timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


user = relationship("User", back_populates="trades")
signal = relationship("Signal", back_populates="trade")