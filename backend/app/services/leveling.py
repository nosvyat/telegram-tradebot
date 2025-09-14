from sqlalchemy.orm import Session
from app.models.level import Level
from app.models.user import User

# Пороговые значения для уровней по суммарному EXP
LEVEL_THRESHOLDS = [0, 100, 300, 700, 1500, 3000, 6000, 10000, 18000, 30000]  # уровни 1..10

def calc_level(total_exp: float) -> int:
    lvl = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS, start=1):
        if total_exp >= threshold:
            lvl = i
        else:
            break
    return lvl

def get_or_create_level(db: Session, user: User) -> Level:
    if not user.level:
        user.level = Level(user_id=user.id, exp=0.0, level=1)
        db.add(user.level)
        db.flush()
    return user.level

def add_exp_for_trade(db: Session, user: User, pnl: float) -> Level:
    # Начисляем EXP только за профит
    gain = max(pnl, 0.0) * 10.0
    lvl = get_or_create_level(db, user)
    lvl.exp += gain
    lvl.level = calc_level(lvl.exp)
    db.flush()
    return lvl
