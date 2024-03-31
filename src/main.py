from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from api.meetings import router as meetings_router
from api.agents import router as agent_router
from db.crud.agents import fill_defaults as fill_agents
from db.crud.meetings import fill_defaults as fill_meetings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await fill_agents()
    await fill_meetings()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(meetings_router)
app.include_router(agent_router)
