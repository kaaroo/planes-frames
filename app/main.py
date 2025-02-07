from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI

from app.config import SCHEDULERS_INTERVAL_S
from app.data_generators.multiple_frames_generator import FramesGenerator
from app.database import Database
from app.db_init import db_setup
from app.mappings import map_dataframes
from app.models import PlaneFrame as PlaneFrameModel
from app.schemas import PlaneDataFrame

fg = FramesGenerator()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


@asynccontextmanager
async def lifespan(application: FastAPI):
    print("Application is starting up...")
    await db_setup(application)
    print("Database models set up.")

    await fg.create_planes()
    print("Planes instances created.")

    print('Setting up scheduler...')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fg.run_frames_generation, trigger=IntervalTrigger(seconds=SCHEDULERS_INTERVAL_S))
    scheduler.start()

    print("Finished app's startup.")

    yield
    print("Application shutdown...")
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {'Project': 'Planes Data Generator App'}


@app.get("/planes", response_model=List[PlaneDataFrame])
async def get_latest_planes_positions():
    frames: List[PlaneFrameModel] = await Database.get_last_positions(list(fg.planes_ids))

    return map_dataframes(frames)


@app.get("/planeHistory", response_model=List[PlaneDataFrame])
async def get_plane_history(icao: str):
    frames: List[PlaneFrameModel] = await Database.get_planes_frames(icao)

    return map_dataframes(frames)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
