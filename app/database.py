from typing import List

from app.models import PlaneFrame as PlaneFrameModel
from app.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB_NAME, POSTGRES_HOSTNAME, POSTGRES_PORT


class Database:
    DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

    @staticmethod
    async def get_last_planes_positions(planes_icaos: List[str]) -> List[PlaneFrameModel]:
        frames = await PlaneFrameModel.filter(plane_id__in=planes_icaos).order_by('-timestamp').limit(len(planes_icaos))

        frames_icaos_set = set([frame.plane_id for frame in frames])
        planes_icaos_set = set(planes_icaos)

        if not frames_icaos_set == planes_icaos_set:
            raise ValueError(
                f"""Unexpected frames results: set of icaos ({str(frames_icaos_set)}) of reset frames 
                is not the same as an input {str(planes_icaos_set)}""")

        return frames

    @staticmethod
    async def get_frames_for_plane(plane_icao: str, number_of_frames: int = 50) -> List[PlaneFrameModel]:
        return await PlaneFrameModel.filter(plane_id=plane_icao).order_by('-timestamp').limit(number_of_frames)
