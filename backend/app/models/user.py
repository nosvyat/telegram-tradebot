from sqlalchemy import String, Integer, BigInteger, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
__tablename__ = "users"


id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
name: Mapped[str | None] = mapped_column(String(255))
photo: Mapped[str | None] = mapped_column(String(512))


binance_api_enc: Mapped[str | None] = mapped_column(Text)
binance_secret_enc: Mapped[str | None] = mapped_column(Text)


auto_trading: Mapped[bool] = mapped_column(Boolean, default=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


level = relationship("Level", back_populates="user", uselist=False)
trades = relationship("Trade", back_populates="user")
signals = relationship("Signal", back_populates="user")