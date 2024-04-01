from typing import Annotated
from fastapi import APIRouter, Depends

from schemas.meetings import AgentSchema
from schemas.meetings import AgentSchema
from schemas.routes import PointSchema
from db.crud.agents import get_agent_by_id
from api.dependencies import JWTAuth

from routing.routing import find_closest_agents
from db.crud.routes import get_all_routes


router = APIRouter(prefix='/agents', tags=["agents"])


@router.get('/')
async def get_agents_handler(point: Annotated[PointSchema, Depends()],
                             user_id: JWTAuth) -> list[AgentSchema | None]:
    resp = []
    routes = await get_all_routes()
    if not routes:
        return resp

    agents = await find_closest_agents(point=point, routes=routes)
    if not agents:
        return resp

    for agent_id, _ in agents:
        agent = await get_agent_by_id(agent_id)
        resp.append(agent)

    return resp
