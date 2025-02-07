import asyncio
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI

from app.database import Database
from app.db_init import db_setup
from app.frames_generators.multiple_frames_generator import FramesGenerator
from app.mappings import map_dataframes
from app.models import PlaneFrame as PlaneFrameModel
from app.schemas import PlaneDataFrame

fg = FramesGenerator()


async def on_startup(application: FastAPI):
    print("App is starting up...")
    await db_setup(application)
    print("Database models set up.")

    await fg.create_planes()
    print("Planes instances created.")

    asyncio.create_task(fg.run_frames_generation())
    print('Frame interval task started.')

    print("Finished app's startup.")


# Handle scheduler shut down
@asynccontextmanager
async def lifespan(application: FastAPI):
    await on_startup(application)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {'Project': 'Planes Data Generator App'}


@app.get("/planes", response_model=List[PlaneDataFrame])
async def get_latest_planes_positions():
    frames: List[PlaneFrameModel] = await Database.get_last_positions(fg.planes_ids)

    return map_dataframes(frames)


@app.get("/planeHistory", response_model=List[PlaneDataFrame])
async def get_plane_history(icao: str):
    frames: List[PlaneFrameModel] = await Database.get_planes_frames(icao)

    return map_dataframes(frames)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
