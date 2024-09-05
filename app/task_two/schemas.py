from pydantic import BaseModel, ConfigDict


class SPrizes(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SPrizesResponse(BaseModel):
    status: str
    prize: SPrizes

    model_config = ConfigDict(from_attributes=True)
