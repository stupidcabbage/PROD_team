import asyncio
from datetime import datetime, timedelta
from typing import Tuple

# from config import external_api_config
from routing.client import client
from schemas.meetings import LocationSchema
from schemas.routes import PointSchema, RouteSchema

graphhopper_url = 'https://graphhopper.com/api/1/'


def generate_graphhopper_url(points: list[Tuple[float, float]]) -> str:
    graph_points = '&point='.join([','.join([str(point[0]), str(point[1])])
                                   for point in points])
    key = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
    print(graph_points)
    return f'{graphhopper_url}route?point={graph_points}&vehicle=car&key={key}'


async def get_route_time(point_a: Tuple[float, float], point_b: Tuple[float, float],
                         point_c: Tuple[float, float]):
    response = await client.get(generate_graphhopper_url([point_a, point_b, point_c]))

    if response.status_code != 200:
        raise RuntimeError(response.json())

    route_data = response.json()
    if 'paths' in route_data or not route_data['paths']:
        time = route_data['paths'][0]['time']
    else:
        raise RuntimeError('ROUTING ERROR')
    return int(time)


async def find_closest_agents(routes: list[RouteSchema], point: PointSchema) -> list[Tuple[int, int]]:
    target_lon, target_lat = point.longitude, point.latitude
    target_time = point.date_time

    agents = []

    for route in routes:
        if route.locations[0].date_time.date() != target_time.date():
            continue
        print(route)
        print(len(route.locations))

        route.locations.sort(key=lambda x: x.date_time)
        if len(route.locations) == 1:
            print(str(route.locations[0].date_time), str(target_time.date))
            left_point_time = route.locations[0].date_time
            route_time = await get_route_time(
                (route.locations[0].latitude,
                 route.locations[0].longitude),
                (target_lat, target_lon),
                (target_lat, target_lon))
            time_delta = timedelta(minutes=(int(route_time) + 30))
            agents.append((route.agent_id, route_time))

        elif route.locations[-1].date_time < target_time:
            print(route.agent_id)
            route_time = await get_route_time(
                (route.locations[-1].latitude,
                 route.locations[-1].longitude),
                (target_lat, target_lon),
                (target_lat, target_lon))
            time_delta = timedelta(milliseconds=route_time, minutes=30)

            print(
                "PUPU", route.locations[-1].date_time, time_delta, target_time)
            if route.locations[-1].date_time + time_delta < target_time:
                agents.append((route.agent_id, route_time))

        else:
            for i in range(1, len(route.locations)):
                right_point_time = route.locations[i].date_time
                left_point_time = route.locations[i - 1].date_time
                print("TIMES", right_point_time, left_point_time, target_time)
                if right_point_time > target_time and left_point_time < target_time:
                    route_time = await get_route_time(
                        (route.locations[i - 1].latitude,
                         route.locations[i - 1].longitude),
                        (target_lat, target_lon),
                        (route.locations[i].latitude,
                         route.locations[i].longitude))
                    print(route_time)
                    time_delta = timedelta(milliseconds=route_time, minutes=30)

                    if left_point_time + time_delta < right_point_time:
                        agents.append((route.agent_id, route_time))
                        break
    print(agents)
    agents = sorted(agents, key=lambda x: x[1])
    return agents[:10]
