from pydantic import BaseModel
from datetime import datetime


class TradeOut(BaseModel):
id: int
user_id: int
signal_id: int
pnl: float
amount: float
timestamp: datetime


class Config:
from_attributes = True