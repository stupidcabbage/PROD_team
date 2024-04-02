from sqlalchemy import insert, select, update

from db.db import new_session
from datetime import datetime
from db.models.routes import Route
from schemas.routes import (RouteSchema, PointSchema)
from schemas.exceptions import BaseDBException


async def get_route(id: int) -> RouteSchema | None:
    try:
        async with new_session.begin() as session:
            stmt = select(Route).where(Route.id == id)
            result = await session.scalar(stmt)
            if result:
                result = result.to_read_model()
            return result
    except:
        raise BaseDBException


async def get_all_routes() -> list[RouteSchema] | None:
    try:
        async with new_session.begin() as session:
            stmt = select(Route)
            result = await session.scalars(stmt)
            if result:
                result = [row.to_read_model() for row in result]
            return result
    except:
        raise BaseDBException


async def add_route(route: RouteSchema) -> RouteSchema | None:
    try:
        async with new_session.begin() as session:
            _data = route.model_dump()
            for i in _data['locations']:
                i['date_time'] = i['date_time'].isoformat()
            _data['date'] = datetime(year=2024, month=4, day=1)
            stmt = insert(Route).values(**_data).returning(Route)
            meeting = (await session.execute(stmt)).one()[0].to_read_model()

            await session.commit()
            await session.flush()
            return meeting
    except:
        raise BaseDBException


async def update_route_points(route_id: int,
                              points: list[PointSchema]) -> PointSchema:
    async with new_session.begin() as session:
        _points = [point.model_dump() for point in points]
        for loc in _points:
            loc['date_time'] = loc['date_time'].isoformat()
        _data = {'locations': _points}
        stmt = (
            update(Route).
            where(Route.id == route_id).
            values(**_data).
            returning(Route)
        )

        route = (await session.execute(stmt)).one()[0].to_read_model()
        print(route)
        return route


async def get_route_by_agent_and_date(agent_id: int, date: datetime) -> RouteSchema | None:
    try:
        async with new_session.begin() as session:
            stmt = select(Route).where(Route.agent_id ==
                                       agent_id).where(Route.date == date)
            result = await session.scalar(stmt)
            if result:
                result = result.to_read_model()
            return result
    except:
        raise BaseDBException


async def fill_defaults() -> None:
    routes = []
    for day in range(1, 20):
        routes_list = [
            Route(date=datetime(year=2024, month=4, day=day), agent_id=1, locations=[
                PointSchema(
                    latitude=37.6208, longitude=55.7539, date_time=datetime(
                        year=2024, month=4, day=day, hour=8, minute=0)).to_dict()
            ]),

            Route(date=datetime(year=2024, month=4, day=day), agent_id=2, locations=[
                PointSchema(
                    latitude=37.6208, longitude=55.7539, date_time=datetime(
                        year=2024, month=4, day=day, hour=8, minute=0)).to_dict()
            ]),

            Route(date=datetime(year=2024, month=4, day=day), agent_id=3, locations=[
                PointSchema(
                    latitude=37.6208, longitude=55.7539, date_time=datetime(
                        year=2024, month=4, day=day, hour=8, minute=0)).to_dict()
            ]),
            Route(date=datetime(year=2024, month=4, day=day), agent_id=4, locations=[
                PointSchema(
                    latitude=37.6155, longitude=55.7558, date_time=datetime(
                        year=2024, month=4, day=day, hour=8, minute=0)).to_dict()
            ]),
        ]

        for route in routes_list:
            routes.append(route)

    async with new_session.begin() as session:
        existing_rows_count = await session.scalar(select(Route).limit(1))

        if not existing_rows_count:
            for route in routes:
                session.add(route)

        await session.commit()
        await session.flush()
