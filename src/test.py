import asyncio
from datetime import datetime

from schemas.meetings import LocationSchema
from routing.routing import find_closest_agents
from schemas.routes import PointSchema, RouteSchema


async def test():
    routes = [
        RouteSchema(agent_id=2, route=[
            PointSchema(
                longitude=37.6208, latitude=55.7539, date_time=datetime(
                    year=2024, month=4, day=1, hour=12, minute=10), meeting_id=1),
            PointSchema(
                longitude=37.6183, latitude=55.7517, date_time=datetime(
                    year=2024, month=4, day=1, hour=16, minute=30), meeting_id=2)
        ]),
        RouteSchema(agent_id=3, route=[
            PointSchema(
                longitude=37.6155, latitude=55.7558, date_time=datetime(
                    year=2024, month=4, day=1, hour=13, minute=45), meeting_id=3),
        ]),
    ]

    await find_closest_agents(routes, LocationSchema(
        name='Test', longitude=36.9163, latitude=56.0060), target_time=datetime(
        year=2024, month=4, day=1, hour=13, minute=45))

    await find_closest_agents(routes, LocationSchema(
        name='Test', longitude=36.9163, latitude=56.0060), target_time=datetime(
        year=2024, month=4, day=1, hour=13, minute=45))


asyncio.run(test())
