from math import radians, degrees, cos, sin, tan, atan2, sqrt
from typing import Tuple

R_MOON = 1737400.0


def to_stereographic(lat: float, lon: float, south_pole: bool = True) -> Tuple[float, float]:
    if south_pole:
        lat = radians(90+lat)
    else:
        lat = radians(90-lat)
    lon = radians(90-lon)
    r = tan(lat/2)*2*R_MOON
    theta = lon
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y


def to_lat_lon(x: float, y: float, south_pole: float = True) -> Tuple[float, float]:
    r = sqrt(x**2 + y**2)
    theta = atan2(y, x)
    lat = degrees(2*atan2(r, 2*R_MOON))
    if south_pole:
        lat = lat-90
    else:
        lat = 90-lat
    lon = 90 - degrees(theta)
    return lat, lon
