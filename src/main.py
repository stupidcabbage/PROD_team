from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

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


# @app.middleware("http")
# async def TestCustomMiddleware(request: Request, call_next):
#     the_headers = request.headers
#     the_body = await request.json()
#
#     print(the_headers)
#     print(the_body)
#
#     response = await call_next(request)
#
#     return response
#
@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    print(f"response_body={response_body.decode()}")
    return Response(content=response_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type)
