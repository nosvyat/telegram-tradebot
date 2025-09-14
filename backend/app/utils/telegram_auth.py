import hmac, hashlib, urllib.parse, time
from fastapi import HTTPException
from app.core.config import settings


BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN


# valid 24 часа
MAX_AGE = 86400


def check_telegram_auth(init_data: str):
parsed = urllib.parse.parse_qs(init_data, strict_parsing=True)
data_check_string = "\n".join(
f"{k}={v[0]}" for k, v in sorted(parsed.items()) if k != "hash"
)
secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
if h != parsed.get("hash", [None])[0]:
raise HTTPException(401, "Invalid Telegram initData signature")


auth_date = int(parsed.get("auth_date", ["0"])[0])
if time.time() - auth_date > MAX_AGE:
raise HTTPException(401, "initData expired")


return {
"telegram_id": int(parsed["id"][0]),
"name": parsed.get("first_name", [""])[0],
"photo": parsed.get("photo_url", [None])[0],
}