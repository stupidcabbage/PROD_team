from datetime import datetime

from pydantic import BaseModel


class PointSchema(BaseModel):
    longitude: float
    latitude: float
    date_time: datetime

    def to_dict(self):
        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S')
        }


class RouteSchema(BaseModel):
    id: int
    agent_id: int
    locations: list[PointSchema]
