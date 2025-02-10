from typing import List, Optional

from app.database.models import PlaneFrame as PlaneFrameDbModel
from app.database.models import Plane as PlaneDbModel
from app.models import PlaneDataFrame, Plane


def _map_dataframe(frame: PlaneFrameDbModel) -> PlaneDataFrame:
    return PlaneDataFrame(
        icao=frame.plane_id,
        alt=frame.alt,
        lon=frame.lon,
        lat=frame.lat,
        speed=frame.speed,
        timestamp=frame.timestamp
    )


def _map_dataframes(frames: List[PlaneFrameDbModel]) -> List[PlaneDataFrame]:
    return [_map_dataframe(frame) for frame in frames]


def _map_plane(plane: PlaneDbModel) -> Plane:
    return Plane(icao=plane.icao)


async def get_or_create_plane(plane: Plane):
    plane, _ = await PlaneDbModel.get_or_create(icao=plane.icao)
    return _map_plane(plane)


async def get_plane(icao: str) -> Optional[Plane]:
    plane = await PlaneDbModel.get(icao=icao)
    return _map_plane(plane) if plane else None


async def save_plane_data_frame(frame: PlaneDataFrame) -> None:
    plane = await PlaneDbModel.get(icao=frame.icao)

    await PlaneFrameDbModel(
        plane=plane,
        speed=frame.speed,
        lon=frame.lon,
        lat=frame.lat,
        alt=frame.alt,
        timestamp=frame.timestamp
    ).save()


async def get_last_planes_positions(planes_icaos: List[str]) -> List[PlaneDataFrame]:
    frames = await PlaneFrameDbModel.filter(plane_id__in=planes_icaos).order_by('-timestamp').limit(len(planes_icaos))
    return _map_dataframes(frames)


async def get_frames_for_plane(plane_icao: str, number_of_frames: int = 50) -> List[PlaneDataFrame]:
    frames = await PlaneFrameDbModel.filter(plane_id=plane_icao).order_by('-timestamp').limit(number_of_frames)
    return _map_dataframes(frames)
