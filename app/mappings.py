from typing import List

from app.models import PlaneFrame as PlaneFrameModel
from app.schemas import PlaneDataFrame

def map_dataframe(frame: PlaneFrameModel) -> PlaneDataFrame:
    return PlaneDataFrame(
        icao=frame.plane_id,
        alt=frame.alt,
        lon=frame.lon,
        lat=frame.lat,
        speed=frame.speed,
        timestamp=frame.timestamp
    )

def map_dataframes(frames: List[PlaneFrameModel] ) -> List[PlaneDataFrame]:
    return [map_dataframe(frame) for frame in frames]