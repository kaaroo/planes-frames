import random
from datetime import datetime, timezone

from app.settings import MAX_SPEED_KM_H, MIN_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, \
    MAX_ALT_METERS, MIN_ALT_METERS
from app.models import PlaneDataFrame

random.seed(0)


class SingleFrameGenerator:
    """
    FrameGenerator class
    """
    plane_id_icao: str

    def __init__(self, plane_id_icao: str):
        self.plane_id_icao = plane_id_icao
        # TODO make new generation dependent on the previous one (only position)

    def generate_random_plane_frame(self) -> PlaneDataFrame:
        return PlaneDataFrame(
            icao=self.plane_id_icao,
            speed=random.uniform(MIN_SPEED_KM_H, MAX_SPEED_KM_H),
            lon=random.uniform(MIN_LONGITUDE, MAX_LONGITUDE),
            lat=random.uniform(MIN_LATITUDE, MAX_LATITUDE),
            alt=random.randrange(MIN_ALT_METERS, MAX_ALT_METERS),
            timestamp=datetime.now(timezone.utc),
        )
