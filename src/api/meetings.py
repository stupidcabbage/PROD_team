from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, status

from api.dependencies import JWTAuth
from db.crud.documents import get_documents
from db.crud.meetings import (add_meeting, cancel_meeting, get_all_meetings,
                              get_meeting_by_id, update_meeting)
from schemas.meetings import MeetingAddSchema, MeetingSchema, MeetingUpdateSchema
from db.crud.routes import get_route_by_agent_and_date, update_route_points
from schemas.routes import PointSchema
from metrics import inc_day_of_week, inc_time_of_day, meetings_count, canceled_meetings_count

router = APIRouter(prefix='/meetings', tags=["meetings"])


@router.post('/', response_model_exclude_none=True)
async def add_meeting_handler(meeting: Annotated[MeetingAddSchema, Body()],
                              user_id: JWTAuth) -> MeetingSchema | None:
    meeting_ret = await add_meeting(user_id, meeting)

    agent_id = meeting.agent_id
    lat = meeting.place.latitude
    lon = meeting.place.longitude
    date_time = meeting.date

    if not agent_id:
        agent_id = 4

    route_data = await get_route_by_agent_and_date(agent_id=agent_id,
                                                   date=datetime(year=date_time.year,
                                                                 month=date_time.month,
                                                                 day=date_time.day))
    if not route_data:
        return None

    _locations = route_data.locations
    _locations.append(PointSchema(date_time=date_time,
                      latitude=lat, longitude=lon))

    meetings_count.inc(1)
    inc_day_of_week(date_time)
    inc_time_of_day(date_time)
    await update_route_points(route_data.id, _locations)
    print(meeting_ret)
    return meeting_ret


@router.get('/')
async def get_meetings_handler(user_id: JWTAuth) -> list[MeetingSchema]:
    meetings = await get_all_meetings(user_id=user_id)  # TODO
    return meetings


@router.get('/{meeting_id}')
async def get_meeting_handler(meeting_id: int,
                              user_id: JWTAuth) -> MeetingSchema | None:
    meeting = await get_meeting_by_id(meeting_id)
    if meeting:
        meeting.documents = await get_documents(
            True if meeting.type == 'ООО' else False)
    return meeting


@router.delete('/{meeting_id}',
               status_code=status.HTTP_204_NO_CONTENT)
async def cancel_meeting_handler(meeting_id: int,
                                 user_id: JWTAuth):
    canceled_meetings_count.inc(1)
    await cancel_meeting(meeting_id, user_id)
    return {"status": "deleted"}


@router.patch("/{meeting_id}")
async def update_meeting_handler(meeting: MeetingUpdateSchema,
                                 meeting_id: int,
                                 user_id: JWTAuth):
    meeting = await update_meeting(user_id, meeting_id, meeting)
    return meeting
