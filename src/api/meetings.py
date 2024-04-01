from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from api.dependencies import JWTAuth
from db.crud.documents import get_documents
from db.crud.meetings import (add_meeting, cancel_meeting, get_all_meetings,
                              get_meeting_by_id, update_meeting)
from schemas.meetings import MeetingAddSchema, MeetingSchema, MeetingUpdateSchema

router = APIRouter(prefix='/meetings', tags=["meetings"])


@router.post('/')
async def add_meeting_handler(meeting: Annotated[MeetingAddSchema, Body()],
                              user_id: JWTAuth) -> MeetingSchema | None:
    meeting = await add_meeting(user_id, meeting)

    agent_id = meeting.agent_id
    lat = meeting.place.latitude
    lon = meeting.place.longitude
    date_time = meeting.date

    if not agent_id:
        agent_id = 1

    route_data = await get_route_by_agent_and_date(agent_id=agent_id,
                                                   date=datetime(year=date_time.year,
                                                                 month=date_time.month,
                                                                 day=date_time.day))
    print(route_data)
    if not route_data:
        return None

    _locations = route_data.locations
    _locations.append(PointSchema(date_time=date_time,
                      latitude=lat, longitude=lon))

    await update_route_points(route_data.id, _locations)


@router.get('/')
async def get_meetings_handler(user_id: JWTAuth) -> list[MeetingSchema]:
    meetings = await get_all_meetings(user_id=user_id)
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
    await cancel_meeting(meeting_id, user_id)
    return {"status": "deleted"}


@router.patch("/{meeting_id}")
async def update_meeting_handler(meeting: MeetingUpdateSchema,
                                 meeting_id: int,
                                 user_id: JWTAuth):
    meeting = await update_meeting(user_id, meeting_id, meeting)
    return meeting
