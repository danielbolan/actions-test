import pytest
from random import random

import lunar_coords as lc


def close_to(a, b, delta=0.00001):
    return abs(a - b) < delta


def test_south_pole():
    lat, lon = -90, 0
    x, y = lc.to_stereographic(lat, lon, south_pole=True)
    assert close_to(x, 0)
    assert close_to(y, 0)
    x, y = 0, 0
    lat, lon = lc.to_lat_lon(x, y, south_pole=True)
    assert close_to(lat, -90)


def test_north_pole():
    lat, lon = 90, 0
    x, y = lc.to_stereographic(lat, lon, south_pole=False)
    assert close_to(x, 0)
    assert close_to(y, 0)
    x, y = 0, 0
    lat, lon = lc.to_lat_lon(x, y, south_pole=False)
    assert close_to(lat, 90)


@pytest.mark.parametrize('lat,lon,south_pole,expected_x,expected_y', [
    (0, 0, True, 0, 2*lc.R_MOON),
    (0, 0, False, 0, 2*lc.R_MOON),
    (0, 90, True, 2*lc.R_MOON, 0),
    (0, 90, False, 2*lc.R_MOON, 0),
    (0, 180, True, 0, -2*lc.R_MOON),
    (0, 180, False, 0, -2*lc.R_MOON),
    (0, 270, True, -2*lc.R_MOON, 0),
    (0, 270, False, -2*lc.R_MOON, 0),
])
def test_equator(lat, lon, south_pole, expected_x, expected_y):
    init_lat, init_lon = lat, lon
    x, y = lc.to_stereographic(lat, lon, south_pole=south_pole)
    assert close_to(x, expected_x)
    assert close_to(y, expected_y)
    lat, lon = lc.to_lat_lon(x, y)
    assert close_to(lat, init_lat)
    assert close_to(lon, init_lon % 360)


def test_southern_random():
    for i in range(1000):
        init_lat, init_lon = random()*90-90, random()*360-180
        x, y = lc.to_stereographic(init_lat, init_lon, south_pole=True)
        lat, lon = lc.to_lat_lon(x, y, south_pole=True)
        assert close_to(lat, init_lat)
        assert close_to(lon % 360, init_lon % 360)


def test_northern_random():
    for i in range(1000):
        init_lat, init_lon = random()*90, random()*360-180
        x, y = lc.to_stereographic(init_lat, init_lon, south_pole=False)
        lat, lon = lc.to_lat_lon(x, y, south_pole=False)
        assert close_to(lat, init_lat)
        assert close_to(lon % 360, init_lon % 360)


def test_full_globe_random():
    for i in range(1000):
        init_lat, init_lon = random()*180-90, random()*360-180
        south = init_lat < 0
        x, y = lc.to_stereographic(init_lat, init_lon, south_pole=south)
        lat, lon = lc.to_lat_lon(x, y, south_pole=south)
        assert close_to(lat, init_lat)
        assert close_to(lon % 360, init_lon % 360)
