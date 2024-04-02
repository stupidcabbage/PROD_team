from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
import prometheus_client
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


@app.get('/metrics')
def get_metrics():
    return Response(media_type='text/plain', content=prometheus_client.generate_latest())
