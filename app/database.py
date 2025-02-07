from typing import List

from app.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB_NAME
from app.models import PlaneFrame as PlaneFrameModel


class Database:
    DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB_NAME}"

    @staticmethod
    async def get_last_positions(planes_icaos: List[str]) -> List[PlaneFrameModel]:
        return await PlaneFrameModel.filter(plane_id__in=planes_icaos).order_by('timestamp').limit(len(planes_icaos))

    @staticmethod
    async def get_planes_frames(plane_icao: str, number_of_frames: int = 50) -> List[PlaneFrameModel]:
        return await PlaneFrameModel.filter(plane_id=plane_icao).order_by('timestamp').limit(number_of_frames)
