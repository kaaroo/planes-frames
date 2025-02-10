from app.data_generators.multiple_frames_generator import MultipleFramesGenerator
from app.service import PlaneService

frames_generator = MultipleFramesGenerator()
plane_service = PlaneService(frames_generator=frames_generator)
