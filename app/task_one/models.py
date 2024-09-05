from typing import Annotated, Optional
from sqlalchemy import ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from datetime import datetime, UTC, date

from app.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class BoostType(PyEnum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    INTELLIGENCE = "intelligence"
    CHARISMA = "charisma"
    PHYSIQUE = "physique"


class Player(Base):
    __tablename__ = "players"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True, index=True)
    first_login: Mapped[Optional[date]] = mapped_column(Date)
    last_login: Mapped[date] = mapped_column(Date, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    points: Mapped[int] = mapped_column(default=0)

    boosts = relationship("Boost", back_populates="player")

    def login(self):
        if self.first_login is None:
            self.first_login = datetime.now(UTC)
        self.last_login = datetime.now(UTC)
        self.points += 1

    def add_boost(self, boost_type: str, amount=1):
        boost = next((b for b in self.boosts if b.boost_type == boost_type), None)
        if boost is None:
            boost = Boost(boost_type=boost_type, amount=amount, player=self)
            self.boosts.append(boost)
        else:
            boost.amount += amount

    def __repr__(self):
        return f"<Player(username='{self.username}', points={self.points})>"


class Boost(Base):
    __tablename__ = "boosts"

    id: Mapped[intpk]
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    boost_type: Mapped[BoostType] = mapped_column(Enum(BoostType))
    amount: Mapped[int] = mapped_column(default=0)

    player = relationship("Player", back_populates="boosts")

    def __repr__(self):
        return f"<Boost(type='{self.boost_type}', amount={self.amount})>"
