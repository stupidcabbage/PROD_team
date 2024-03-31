from typing import Annotated

from fastapi import APIRouter, Body
from schemas.meetings import MeetingAddSchema, MeetingSchema
from api.dependencies import JWTAuth
from db.crud.meetings import add_meeting, get_all_meetings, get_meeting_by_id
from db.crud.documents import get_documents


router = APIRouter(prefix='/meetings', tags=["meetings"])


@router.post('/')
async def add_meeting_handler(meeting: Annotated[MeetingAddSchema, Body()],
                              user_id: JWTAuth) -> MeetingSchema | None:
    meeting = await add_meeting(user_id, meeting)
    return meeting


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
