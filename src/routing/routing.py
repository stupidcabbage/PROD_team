from datetime import datetime
from typing import Tuple
from config import external_api_config
from routing.client import client
from schemas.meetings import LocationSchema
from schemas.routes import RouteSchema


graphhopper_url = 'https://graphhopper.com/api/1/'


def generate_graphhopper_url(points: list[Tuple[float, float]]) -> str:
    graph_points = '&point='.join([','.join([str(point[0]), str(point[1])])
                                   for point in points])

    return f'{graphhopper_url}route?point={graph_points}&vehicle=car&key={external_api_config.graphhopper_key}'


async def get_route_time(point_a: Tuple[float, float], point_b: Tuple[float, float],
                         point_c: Tuple[float, float]):
    response = await client.get(generate_graphhopper_url([point_a, point_b, point_c]))

    if response.status_code == 400:
        raise RuntimeError(Templates.NO_ROUTE.value)

    if response.status_code != 200:
        raise RuntimeError(Templates.ROUTING_ERROR.value)

    route_data = response.json()

    if 'paths' in route_data or not route_data['paths']:
        encoded_polyline = route_data['paths'][0]['points']
    else:
        raise RuntimeError(Templates.NO_ROUTE.value)


def find_closest_agents(routes: list[RouteSchema], location: LocationSchema, target_time: datetime):
    target_lon, target_lat = location.longitude, location.latitude

    for route in routes:
        for i in range(1, len(route.route)):
            right_point_time = route.route[i].date_time
            left_point_time = route.route[i - 1].date_time
            if right_point_time < target_time and left_point_time > target_time:
