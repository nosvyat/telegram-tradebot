from sqlalchemy.orm import Session
from app.models.signal import Signal
from app.models.trade import Trade
from app.models.user import User
from app.core.binance_api import BinanceSvc
from app.services.leveling import add_exp_for_trade
from datetime import datetime

class TradingService:
    @staticmethod
    def execute_signal(db: Session, user: User, signal: Signal) -> Trade:
        side = "BUY" if signal.type.value == "buy" else "SELL"
        # Упрощение: количество = amount из сигнала
        resp = BinanceSvc.market_order(user, symbol=signal.symbol, side=side, quantity=signal.amount)

        # Попробуем вытащить среднюю цену исполнения, если биржа вернула fills
        executed_price = None
        try:
            fills = resp.get("fills") or []
            if fills:
                qty_sum = sum(float(f["qty"]) for f in fills)
                if qty_sum > 0:
                    executed_price = sum(float(f["price"]) * float(f["qty"]) for f in fills) / qty_sum
        except Exception:
            executed_price = None  # оставим None, если не получилось

        trade = Trade(
            user_id=user.id,
            signal_id=signal.id,
            side=side,
            amount=signal.amount,
            executed_price=executed_price,
            pnl=0.0,
            is_closed=False,
        )
        db.add(trade)
        db.flush()   # получим trade.id
        signal.status = signal.status.EXECUTED
        db.commit()
        db.refresh(trade)
        return trade

    @staticmethod
    def close_trade(db: Session, user: User, trade: Trade, realized_pnl: float) -> Trade:
        # Фиксируем PnL и закрываем сделку
        trade.pnl = realized_pnl
        trade.is_closed = True
        trade.closed_at = datetime.utcnow()

        # Начисляем EXP за профит
        add_exp_for_trade(db, user, realized_pnl)

        db.commit()
        db.refresh(trade)
        return trade
