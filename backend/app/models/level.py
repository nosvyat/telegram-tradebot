from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.core.database import Base

class Level(Base):
    __tablename__ = "levels"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    exp: Mapped[float] = mapped_column(default=0.0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="level")
