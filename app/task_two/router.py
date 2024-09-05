import csv
from io import StringIO
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.task_two.dao import LevelPrizeDAO, AllPlayerDataDAO
from app.task_two.schemas import SPrizesResponse

router = APIRouter(
    prefix="/players",
    tags=["Игроки"],
    responses={404: {"description": "Not found"}},
)


@router.post("/assign_prize/")
async def assign_prize(player_id: int, level_id: int, prize_id: int) -> SPrizesResponse:
    """
    Присвоить игроку награду

    Args:   
        player_id (int): идентификатор игрока,  
        level_id (int): идентификатор уровня,   
        prize_id (int): идентификатор награды

    Raises:    
        HTTPException: если игрок не прошёл уровень или награды не существует

    Returns:    
        SPrizesResponse: статус и идентификатор награды
    """
    prize = await LevelPrizeDAO.assign_prize(player_id, level_id, prize_id)
    if prize:
        return {"статус": "присвоено", "награда": prize}
    else:
        raise HTTPException(status_code=400, detail="Игрок не прошёл уровень или награды не существует")
        # на самом деле правильнее вернуть более развёрнутый ответ, т.к. может не существовать
        # не только награды, но и уровня с игроком


@router.get("/export_data/", response_class=StreamingResponse)
async def export_player_data():
    """
    Экспорт данных об игроках

    Returns:    
        StreamingResponse: CSV файл с данными об игроках
    """
    player_data = await AllPlayerDataDAO.get_all_player_data()
    
    # объект StringIO для записи CSV в память
    output = StringIO()
    writer = csv.writer(output)

    # заголовки
    headers = [
        "player_id",
        "level_title",
        "is_completed",
        "prize_title"
    ]
    writer.writerow(headers)

    # запись данных
    for row in player_data:
        writer.writerow([
            row.player_id,
            row.level_title,
            "Пройден" if row.is_completed else "Не пройден",
            row.prize_title if row.prize_title else "Нет награды"
        ])

    output.seek(0) # перемещение указателя в начало файла

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=player_data.csv"}
    )
