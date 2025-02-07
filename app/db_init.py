from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

from app.database import Database

async def db_setup(application: FastAPI):
    Tortoise.init_models(["app.models"], "models")
    await RegisterTortoise(
        app=application,
        db_url=Database.DATABASE_URL,
        modules={"models": ["app.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
        use_tz=False,
        timezone='UTC',
    )