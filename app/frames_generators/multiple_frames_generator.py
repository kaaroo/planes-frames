import asyncio
from datetime import datetime, timezone
from shutil import get_terminal_size
from typing import Dict



from app.models import Plane as PlaneModel
from app.models import PlaneFrame as PlaneFrameModel
from app.frames_generators.single_frame_generator import FrameGenerator
from app.schemas import PlaneDataFrame
from app.frames_generators.utils import get_planes_ids


class FramesGenerator:
    INTERVAL_S = 10

    def __init__(self):
        self.__planes_ids = set()
        self.__planes_generators: Dict[str, FrameGenerator] = {}

    @property
    def planes_ids(self):
        return self.__planes_ids

    async def create_planes(self):
        self.__planes_ids = get_planes_ids()
        self.__planes_generators = {
            plane_id: FrameGenerator(plane_id) for plane_id in self.__planes_ids
        }

        for plane_icao in self.__planes_ids:
            await PlaneModel.get_or_create(icao=plane_icao)

    async def run_frames_generation(self):
        await asyncio.sleep(self.INTERVAL_S)

        if len(self.__planes_ids) == 0:
            raise ValueError('List of planes should not be empty!')

        for plane_id in self.__planes_ids:
            await self._create_plane_frame_data(plane_id)

    async def _create_plane_frame_data(self, plane_frame_icao: str):
        plane = await PlaneModel.get(icao=plane_frame_icao)

        plane_data_frame: PlaneDataFrame = self.__planes_generators[plane_frame_icao].generate_random_plane_frame()

        plane_data_frame: PlaneFrameModel = PlaneFrameModel(
            plane=plane,
            speed=plane_data_frame.speed,
            lon=plane_data_frame.lon,
            lat=plane_data_frame.lat,
            alt=plane_data_frame.alt,
            timestamp=plane_data_frame.timestamp
        )
        await plane_data_frame.save()
