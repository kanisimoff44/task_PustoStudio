from typing import Annotated
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date

from app.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class Player(Base):
    __tablename__ = "players"

    id: Mapped[intpk]
    player_id: Mapped[int] = mapped_column(unique=True)


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[intpk]
    title: Mapped[str]
    order: Mapped[int] = mapped_column(default=0)


class Prize(Base):
    __tablename__ = "prizes"

    id: Mapped[intpk]
    title: Mapped[str]


class PlayerLevel(Base):
    __tablename__ = "player_levels"

    id: Mapped[intpk]
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"))
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))
    completed: Mapped[date] = mapped_column(Date)
    is_completed: Mapped[bool] = mapped_column(default=False)
    score: Mapped[int] = mapped_column(default=0)

    player: Mapped[Player] = relationship("Player")
    level: Mapped[Level] = relationship("Level")


class LevelPrize(Base):
    __tablename__ = "level_prizes"

    id: Mapped[intpk]
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id", ondelete="CASCADE"))
    prize_id: Mapped[int] = mapped_column(ForeignKey("prizes.id", ondelete="CASCADE"))
    received: Mapped[date] = mapped_column(Date)

    level: Mapped[Level] = relationship("Level")
    prize: Mapped[Prize] = relationship("Prize")
