from typing import Tuple
from config import external_api_config
from src.schemas.meetings import LocationSchema
from src.schemas.routes import RouteSchema


graphhopper_url = 'https://graphhopper.com/api/1/'


def generate_graphhopper_url(points: list[Tuple[float, float]]) -> str:
    graph_points = '&point='.join([','.join([str(point[0]), str(point[1])])
                                   for point in points])

    return f'{graphhopper_url}route?point={graph_points}&vehicle=car&key={external_api_config.graphhopper_key}'


def find_closest_agent(routes: list[RouteSchema], location: LocationSchema):
    ...
