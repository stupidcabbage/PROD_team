from typing import Tuple
from config import external_api_config


graphhopper_url = 'https://graphhopper.com/api/1/'


def generate_graphhopper_url(points: list[Tuple[float, float]]) -> str:
    points = '&point='.join([','.join([str(point[0]), str(point[1])])
                             for point in points])

    return f'{graphhopper_url}route?point={points}&vehicle=car&key={external_api_config.graphhopper_key}'
