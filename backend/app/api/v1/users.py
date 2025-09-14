from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.database import get_db
from app.core.security import decrypt_secret, encrypt_secret, decode_token
from app.models.user import User
from app.schemas.user import UserOut
from app.core.binance_api import BinanceSvc


router = APIRouter(prefix="/users", tags=["users"])
auth_scheme = HTTPBearer()


def current_user(creds: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)) -> User:
payload = decode_token(creds.credentials)
user_id = int(payload.get("sub"))
user = db.query(User).get(user_id)
if not user:
raise HTTPException(401, "Invalid token")
return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
return user


@router.post("/me/binance")
def update_binance_keys(api_key: str, api_secret: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
user.binance_api_enc = encrypt_secret(api_key)
user.binance_secret_enc = encrypt_secret(api_secret)
db.commit()
return {"ok": True}


@router.post("/me/auto")
def set_auto_trading(enabled: bool, db: Session = Depends(get_db), user: User = Depends(current_user)):
user.auto_trading = enabled
db.commit()
return {"auto_trading": user.auto_trading}


@router.get("/me/balance")
def balance(user: User = Depends(current_user)):
return BinanceSvc.get_balance(user)