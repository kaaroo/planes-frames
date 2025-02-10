from app.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOSTNAME, POSTGRES_PORT, POSTGRES_DB_NAME
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise

_DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"


async def db_setup(application: FastAPI):
    Tortoise.init_models(["app.database.models"], "models")

    db_url = _DATABASE_URL

    await RegisterTortoise(
        app=application,
        db_url=db_url,
        modules={"models": ["app.database.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
        use_tz=False,
        timezone='UTC',
    )
