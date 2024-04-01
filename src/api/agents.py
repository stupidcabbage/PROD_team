from typing import Annotated
from fastapi import APIRouter, Depends

from db.crud.agents import get_best_agent
from schemas.meetings import AgentSchema
from schemas.meetings import AgentSchema, LocationSchema, MeetingAddSchema, MeetingSchema
from schemas.routes import PointSchema
from db.crud.agents import get_agent_by_id
from api.dependencies import JWTAuth


router = APIRouter(prefix='/agents', tags=["agents"])


@router.get('/')
async def get_agents_handler(point: Annotated[PointSchema, Depends()],
                             user_id: JWTAuth) -> list[AgentSchema | None] | None:
    return [await get_agent_by_id(4)]
