from sqlalchemy import insert, select, update

from db.db import new_session
from datetime import datetime
from db.models.routes import Route
from schemas.routes import (RouteSchema, PointSchema)
from sqlalchemy.exc import IntegrityError

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
    try:
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

            meeting = (await session.execute(stmt)).one()[0].to_read_model()
            return meeting
    except:
        raise BaseDBException
