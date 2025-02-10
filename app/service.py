from typing import List

from app.data_generators.multiple_frames_generator import MultipleFramesGenerator
from app.database import plane_repository
from app.models import PlaneDataFrame


class PlaneService:
    _frames_generator: MultipleFramesGenerator

    def __init__(self, frames_generator: MultipleFramesGenerator):
        self._frames_generator = frames_generator

    async def get_latest_planes_positions(self) -> List[PlaneDataFrame]:
        planes_ids = list(self._frames_generator.planes_ids)
        frames = await plane_repository.get_last_planes_positions(planes_ids)

        frames_icaos_set = set([frame.icao for frame in frames])
        planes_icaos_set = set(planes_ids)

        if not frames_icaos_set == planes_icaos_set:
            raise ValueError(
                f"""Unexpected frames results: set of icaos ({str(frames_icaos_set)}) of reset frames 
                is not the same as an input {str(planes_icaos_set)}""")

        return frames

    async def get_plane_history(self, icao: str) -> List[PlaneDataFrame]:
        return await plane_repository.get_frames_for_plane(icao)
