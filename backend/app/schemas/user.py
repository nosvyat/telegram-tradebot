from pydantic import BaseModel


class UserBase(BaseModel):
telegram_id: int
name: str | None = None
photo: str | None = None


class UserCreate(UserBase):
pass


class UserOut(UserBase):
id: int
auto_trading: bool


class Config:
from_attributes = True