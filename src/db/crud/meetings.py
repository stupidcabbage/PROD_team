from datetime import datetime
from random import randint

from sqlalchemy import insert, select, update

from db.crud.agents import get_best_agent
from db.crud.documents import get_documents
from db.db import new_session
from db.models.meetings import Meeting
from schemas.meetings import (MeetingAddSchema, MeetingSchema,
                              MeetingUpdateSchema)
from schemas.exceptions import BaseDBException
from utils import get_client
from sqlalchemy.exc import IntegrityError


async def get_meeting_by_id(id: int) -> MeetingSchema | None:
    try:
        async with new_session.begin() as session:
            stmt = select(Meeting).where(Meeting.id == id)
            result = await session.scalar(stmt)
            if result:
                result = result.to_read_model()
            return result
    except IntegrityError:
        raise BaseDBException


async def get_all_meetings(user_id: int) -> list[MeetingSchema] | None:
    try:
        async with new_session.begin() as session:
            stmt = (
                select(Meeting).
                where(Meeting.user_id == user_id).
                where(Meeting.is_canceled == False).
                order_by(Meeting.date)
            )
            result = await session.scalars(stmt)
            if result:
                result = [row.to_read_model() for row in result]
            return result
    except IntegrityError:
        raise BaseDBException


async def add_meeting(user_id: int,
                      meeting: MeetingAddSchema) -> MeetingSchema | None:
    try:
        async with new_session.begin() as session:
            _data = meeting.model_dump()
            del _data["place"]
            _data["location_lon"] = meeting.place.longitude
            _data["location_lat"] = meeting.place.latitude
            _data["location_name"] = meeting.place.name
            _data["user_id"] = user_id

            client = get_client(user_id)
            _data["type"] = client["type"]
            _data["agent_id"] = randint(2, 5)
            _data['is_canceled'] = False

            stmt = insert(Meeting).values(_data).returning(Meeting)
            meeting = (await session.execute(stmt)).one()[0].to_read_model()
            documents = await get_documents(
                True if client["type"] == "ООО" else False)
            meeting.documents = documents
            await session.commit()
            await session.flush()
            return meeting
    except:
        raise BaseDBException


async def update_meeting(user_id: int,
                         meeting_id: int,
                         meeting: MeetingUpdateSchema) -> MeetingSchema:
    try:
        async with new_session.begin() as session:
            _data = {}
            if meeting.place:
                _data["location_lon"] = meeting.place.longitude
                _data["location_lat"] = meeting.place.latitude
                _data["location_name"] = meeting.place.name

            meeting_data = meeting.model_dump()
            if meeting.participants:
                _data["participants"] = meeting_data["participants"]
            if meeting.date:
                _data["date"] = meeting_data["date"]
            stmt = (
                update(Meeting).
                where(Meeting.user_id == user_id).
                where(Meeting.id == meeting_id).
                values(**_data).
                returning(Meeting)
            )

            meeting_updated = (await session.execute(stmt)).one()[0].to_read_model()
            await session.commit()
            return meeting_updated
    except:
        raise BaseDBException


async def cancel_meeting(meeting_id: int,
                         user_id: int) -> None:
    try:
        async with new_session.begin() as session:
            stmt = (
                update(Meeting).
                where(Meeting.id == meeting_id).
                where(Meeting.user_id == user_id).
                values(is_canceled=True)
            )
            await session.execute(stmt)
            await session.commit()
    except:
        raise BaseDBException


async def fill_defaults() -> None:
    meetings = [
        Meeting(
            user_id=1,
            agent_id=1,
            date=datetime(
                year=2024, month=4, day=1, hour=12, minute=10),
            type='ООО',
            participants=[
                {'name': 'Иванов Иван', 'position': 'Бухгалтер', 'phone_number': '+79851187385'}],
            location_lon=55.3,
            location_lat=46.3,
            location_name='Московская область, Нахабино, Красноармейская 5к1',
            is_canceled=False,
        )
    ]
    async with new_session.begin() as session:
        existing_rows_count = await session.scalar(select(Meeting).limit(1))

        if not existing_rows_count:
            for meeting in meetings:
                session.add(meeting)

        await session.commit()
        await session.flush()
    #
    # id: Mapped[int] = mapped_column(
    #     BIGINT, primary_key=True, autoincrement=True)
    #
    # user_id: Mapped[int] = mapped_column()
    # agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id'))
    # agent: Mapped["Agent"] = relationship(lazy="selectin")
    # date: Mapped[datetime] = mapped_column()
    # type: Mapped[str] = mapped_column()
    # participants: Mapped[JSON] = mapped_column(JSON)
    # location_lon: Mapped[float] = mapped_column(FLOAT)
    # location_lat: Mapped[float] = mapped_column(FLOAT)
    # location_name: Mapped[str] = mapped_column()
    #
