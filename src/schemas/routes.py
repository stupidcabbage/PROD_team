from datetime import datetime

from pydantic import BaseModel


class PointSchema(BaseModel):
    meeting_id: int  # если пригодится
    longitude: float
    latitude: float
    date_time: datetime


class RouteSchema(BaseModel):
    agent_id: int
    locations: list[PointSchema]
