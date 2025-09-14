from binance.spot import Spot as BinanceClient
from app.core.security import decrypt_secret
from app.models.user import User


class BinanceSvc:
@staticmethod
def _client(user: User) -> BinanceClient:
api_key = decrypt_secret(user.binance_api_enc)
api_secret = decrypt_secret(user.binance_secret_enc)
return BinanceClient(api_key=api_key, api_secret=api_secret)


@staticmethod
def get_balance(user: User) -> list[dict]:
client = BinanceSvc._client(user)
info = client.account()
return info.get("balances", [])


@staticmethod
def market_order(user: User, symbol: str, side: str, quantity: float) -> dict:
client = BinanceSvc._client(user)
return client.new_order(symbol=symbol, side=side.upper(), type="MARKET", quantity=quantity)