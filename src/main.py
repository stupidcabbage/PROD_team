from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from sqlalchemy.ext import asyncio
from api.agents import router as agent_router
from api.meetings import router as meetings_router
from api.products import router as products_router
from db.crud.agents import fill_defaults as fill_agents
from db.crud.meetings import fill_defaults as fill_meetings
from db.crud.agents import fill_defaults as fill_agents
from db.crud.routes import fill_defaults as fill_routes
from db.crud.products import fill_defaults as fill_products
from api.exceptions import db_exception_handler
from schemas.exceptions import BaseDBException
# from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST


# Define Prometheus metrics
requests_counter = Counter('http_requests_total',
                           'Total HTTP Requests', ['method', 'endpoint'])
processing_time = Gauge('http_request_processing_seconds',
                        'HTTP Request Processing Time')


@asynccontextmanager
async def lifespan(app: FastAPI):
    await fill_agents()
    await fill_meetings()
    # await fill_products()
    await fill_routes()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(meetings_router)
app.include_router(agent_router)
app.include_router(products_router)
# Instrumentator().instrument(app).expose(app)
# app.add_exception_handler(BaseDBException, db_exception_handler)


@app.get("/metrics")
async def metrics():
    # Generate and return the latest Prometheus metrics
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


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
    print(await request.body())
    response = await call_next(request)
    print(request.headers)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    print(f"response_body={response_body.decode()}")
    return Response(content=response_body, status_code=response.status_code,
                    headers=dict(response.headers), media_type=response.media_type)
