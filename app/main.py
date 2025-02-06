# Set up the scheduler
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import List

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler  # runs tasks in the background
from apscheduler.triggers.interval import IntervalTrigger  # <-- CHANGED IMPORT
from fastapi import FastAPI, Response

from app.schemas import PlaneDataFrame
from app.tasks import FramesGenerator

fg = FramesGenerator()

global data

# The task to run
def generate_planes_data_task():
    global data
    data = fg.generate_new_planes_data()


# Set up the scheduler
# TODO compare (scheduler) with other approaches
scheduler = BackgroundScheduler()
trigger = IntervalTrigger(seconds=1)
scheduler.add_job(generate_planes_data_task, trigger)
scheduler.start()

app = FastAPI()

# Handle scheduler shut down
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()

@app.get("/")
async def root():
    return {'Project': 'Planes Data Generator App'}

@app.get("/planes", response_model=List[PlaneDataFrame])
async def get_latest_planes_positions():
    return data

@app.get("/planeHistory/{icao}", response_model=List[PlaneDataFrame])
def get_plane_history(plane_icao: str):
    # TODO
    raise NotImplemented()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
