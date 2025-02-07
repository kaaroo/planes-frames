from typing import Dict

from app.data_generators.single_frame_generator import FrameGenerator
from app.data_generators.utils import get_planes_ids
from app.models import Plane as PlaneModel
from app.models import PlaneFrame as PlaneFrameModel
from app.schemas import PlaneDataFrame


class FramesGenerator:

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
        if len(self.__planes_ids) == 0:
            raise ValueError('Generating frames error: planes (icaos) should exist at this point')

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
