from fastapi import APIRouter

from schemas.meetings import AgentSchema
from db.crud.agents import get_best_agent

router = APIRouter(prefix='/agents', tags=["agents"])


@router.get('/')
async def get_agents() -> AgentSchema | None:
    return await get_best_agent()
