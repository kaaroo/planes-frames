import logging
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from app.context import frames_generator, plane_service
from app.database.settings import db_setup
from app.models import PlaneDataFrame
from app.settings import SCHEDULERS_INTERVAL_S

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Application is starting up...")
    await db_setup(application)
    logger.info("Database models set up.")

    await frames_generator.create_planes()
    logger.info("Planes instances created.")

    logger.info('Setting up scheduler...')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(frames_generator.run_frames_generation, trigger=IntervalTrigger(seconds=SCHEDULERS_INTERVAL_S))
    scheduler.start()

    logger.info("Finished app's startup.")

    yield
    logger.info("Application shutdown...")
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {'Project': 'Planes Data Generator App'}


@app.get("/planes", response_model=List[PlaneDataFrame])
async def get_latest_planes_positions():
    return await plane_service.get_latest_planes_positions()


@app.get("/planeHistory", response_model=List[PlaneDataFrame])
async def get_plane_history(icao: str):
    return await plane_service.get_plane_history(icao)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
