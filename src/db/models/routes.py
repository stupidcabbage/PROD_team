from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import BIGINT, JSON, FLOAT, ForeignKey

from db.db import Model
from db.models.agents import Agent
from schemas.meetings import MeetingSchema, LocationSchema, ParticipantSchema


class Route(Model):
    __tablename__ = 'routes'

    id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=True)

    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    date: Mapped[datetime] = mapped_column()
    locations: Mapped[JSON] = mapped_column(JSON)

    def __repr__(self) -> str:
        return f"Meeting(id: {self.id!r}, date: {self.date!r})"

    def to_read_model(self) -> MeetingSchema:
        return MeetingSchema(
            id=self.id,
            agent=self.agent.to_read_model(),  # noqa #type: ignore
            participants=[ParticipantSchema(name=i["name"],
                                            position=i["position"],
                                            phone_number=i["phone_number"]) for i in self.participants],
            date=self.date,
            place=LocationSchema(
                latitude=self.location_lat,
                longitude=self.location_lon,
                name=self.location_name)
            )
