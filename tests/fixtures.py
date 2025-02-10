import random
import string

from app.models import PlaneDataFrame
from datetime import datetime

from app.settings import MAX_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, MIN_ALT_METERS, \
    MAX_ALT_METERS, MIN_SPEED_KM_H


def some_icao() -> str:
    return "".join(random.choice(string.ascii_uppercase) for _ in range(4))


def some_plane_data_frame() -> PlaneDataFrame:
    return PlaneDataFrame(
        icao=some_icao(),
        speed=random.uniform(MIN_SPEED_KM_H, MAX_SPEED_KM_H),
        lon=random.uniform(MIN_LONGITUDE, MAX_LONGITUDE),
        lat=random.uniform(MIN_LATITUDE, MAX_LATITUDE),
        alt=random.randint(MIN_ALT_METERS, MAX_ALT_METERS),
        timestamp=datetime.now()
    )
