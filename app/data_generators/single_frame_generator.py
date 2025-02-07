import random
from datetime import datetime, timezone

from app.config import MIN_SPEED_KM_H, MAX_SPEED_KM_H, MIN_LONGITUDE, MIN_LATITUDE, MAX_LONGITUDE, MAX_LATITUDE, \
    MAX_ALT_METERS, MIN_ALT_METERS
from app.schemas import PlaneDataFrame

random.seed(0)


class FrameGenerator:
    """
    FrameGenerator class
    """

    def __init__(self, plane_id_icao: str):
        self.plane_id_icao = plane_id_icao

        # TODO make new generation dependent on the previous one (only position)

    def generate_random_plane_frame(self) -> PlaneDataFrame:
        dt = datetime.now(timezone.utc)  # TODO map to the timestamp in db
        speed = random.uniform(MIN_SPEED_KM_H, MAX_SPEED_KM_H)
        longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)
        latitude = random.uniform(MIN_LATITUDE, MAX_LATITUDE)
        alt_meters = (random.randrange(MIN_ALT_METERS, MAX_ALT_METERS))

        return PlaneDataFrame(
            icao=self.plane_id_icao,
            speed=speed,
            lon=longitude,
            lat=latitude,
            alt=alt_meters,
            timestamp=dt,
        )
