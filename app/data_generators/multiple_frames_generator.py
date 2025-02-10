from typing import Dict

from app.data_generators.single_frame_generator import SingleFrameGenerator
from app.data_generators.utils import generate_plane_ids
from app.database import plane_repository
from app.models import Plane


class MultipleFramesGenerator:
    __planes_ids: set[str]
    __planes_generators: Dict[str, SingleFrameGenerator]

    def __init__(self):
        self.__planes_ids = set()
        self.__planes_generators = {}

    @property
    def planes_ids(self) -> set[str]:
        return self.__planes_ids

    async def create_planes(self):
        self.__planes_ids = generate_plane_ids()
        self.__planes_generators = {
            plane_id: SingleFrameGenerator(plane_id) for plane_id in self.__planes_ids
        }

        for plane_icao in self.__planes_ids:
            await plane_repository.get_or_create_plane(Plane(icao=plane_icao))

    async def run_frames_generation(self):
        if len(self.__planes_ids) == 0:
            raise ValueError('Generating frames error: planes (icaos) should exist at this point')

        for plane_id in self.__planes_ids:
            await self._create_plane_frame_data(plane_id)

    async def _create_plane_frame_data(self, plane_frame_icao: str):
        frame = self.__planes_generators[plane_frame_icao].generate_random_plane_frame()
        await plane_repository.save_plane_data_frame(frame)
