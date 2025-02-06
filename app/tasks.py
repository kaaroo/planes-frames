import asyncio
from typing import Dict, List

from app.plane_frame_generator import PlanFrameGenerator
from app.schemas import PlaneDataFrame
from app.utils import get_planes_ids


class FramesGenerator:

    def __init__(self):
        self.planes_ids = get_planes_ids()
        self.planes_generators : Dict[str, PlanFrameGenerator]= {
            plane_id: PlanFrameGenerator(plane_id) for plane_id in self.planes_ids
        }

    def generate_new_planes_data(self) -> List[PlaneDataFrame]:
        recent_data = []
        for plane_id, plane_generator in self.planes_generators.items():
            plane_frame = plane_generator.generate_random_plane_frame()

            recent_data.append(plane_frame)

        return recent_data

