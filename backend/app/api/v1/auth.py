from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import Token
from app.utils.telegram_auth import check_telegram_auth


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/telegram", response_model=Token)
def login_telegram(init_data: str, db: Session = Depends(get_db)):
info = check_telegram_auth(init_data)
user = db.query(User).filter(User.telegram_id == info["telegram_id"]).first()
if not user:
user = User(telegram_id=info["telegram_id"], name=info["name"], photo=info["photo"])
db.add(user)
db.commit()
db.refresh(user)
token = create_access_token({"sub": str(user.id)})
return Token(access_token=token)