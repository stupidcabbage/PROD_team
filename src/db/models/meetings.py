import json
from datetime import datetime

from sqlalchemy import BIGINT, FLOAT, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.db import Model
from db.models.agents import Agent
from schemas.meetings import (BusinessType, LocationSchema, MeetingSchema,
                              ParticipantSchema)


class Meeting(Model):
    __tablename__ = 'meetings'

    id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column()
    agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    agent: Mapped["Agent"] = relationship(lazy="selectin")
    date: Mapped[datetime] = mapped_column()
    type: Mapped[str] = mapped_column()
    participants: Mapped[JSON] = mapped_column(JSON)
    location_lon: Mapped[float] = mapped_column(FLOAT)
    location_lat: Mapped[float] = mapped_column(FLOAT)
    location_name: Mapped[str] = mapped_column()
    is_canceled: Mapped[bool] = mapped_column()

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
                name=self.location_name),
            is_canceled=self.is_canceled,
            type=BusinessType.organisation if self.type == 'ООО' else BusinessType.individual
            )
