from sqlalchemy.future import select
from datetime import datetime, UTC

from app.task_two.models import PlayerLevel, LevelPrize, Level, Prize
from app.database import async_session_maker


class PlayerLevelDAO:
    model = PlayerLevel

    @classmethod
    async def get_player_level(cls, player_id: int, level_id: int):
        async with async_session_maker() as session:
            query = (
                select(PlayerLevel.__table__.c)
                .where(
                    PlayerLevel.player_id == player_id,
                    PlayerLevel.level_id == level_id
                )
            )
            result = await session.execute(query)
            return result.mappings().first()


class LevelPrizeDAO:
    model = LevelPrize
    
    @classmethod
    async def assign_prize(cls, player_id: int, level_id: int, prize_id: int) -> None:
        async with async_session_maker() as session:
            player_level = await PlayerLevelDAO.get_player_level(player_id, level_id)
            
            if player_level and player_level.is_completed:
                new_level_prize = LevelPrize(
                    level_id=level_id,
                    prize_id=prize_id,
                    received=datetime.now(UTC)
                )
                session.add(new_level_prize)
                await session.commit()
                return new_level_prize
            else:
                return None


class AllPlayerDataDAO:
    model = PlayerLevel
    
    @classmethod
    async def get_all_player_data(cls):
        """
        SELECT 
            players.player_id,
            levels.title,
            player_levels.is_completed,
            prizes.title
        FROM
            player_levels
        JOIN
            level ON player_levels.level_id = level.id
        LEFT JOIN
            level_prizes ON level_prizes.level_id = level.id
        LEFT JOIN
            prizes ON level_prizes.prize_id = prizes.id
        """
        async with async_session_maker() as session:
            query = (
                select(
                    PlayerLevel.player_id,
                    Level.title.label("level_title"),
                    PlayerLevel.is_completed,
                    Prize.title.label("prize_title")
                )
                .join(Level, PlayerLevel.level_id == Level.id)
                .outerjoin(LevelPrize, LevelPrize.level_id == Level.id)
                .outerjoin(Prize, LevelPrize.prize_id == Prize.id)
            )

            result = await session.execute(query)

            return result.mappings().all()
