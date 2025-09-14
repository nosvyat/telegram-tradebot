from pydantic import BaseModel
from datetime import datetime
from app.models.signal import SignalStatus, SignalType


class SignalIn(BaseModel):
symbol: str
type: SignalType
price: float
amount: float = 0.0


class SignalOut(SignalIn):
id: int
user_id: int
timestamp: datetime
status: SignalStatus


class Config:
from_attributes = True