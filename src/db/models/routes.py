from datetime import datetime

from sqlalchemy import BIGINT, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Model
from schemas.routes import PointSchema, RouteSchema


class Route(Model):
    __tablename__ = 'routes'

    id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=True)

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    date: Mapped[datetime] = mapped_column()
    locations: Mapped[JSON] = mapped_column(JSON)

    def to_read_model(self) -> RouteSchema:
        return RouteSchema(id=self.id, agent_id=self.agent_id, date=self.date,
                           locations=[PointSchema(**location) for location in self.locations])
