from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PointSchema(BaseModel):
    meeting_id: int
    longitude: float
    latitude: float
    date_time: datetime


class RouteSchema(BaseModel):
    route: list[PointSchema]
