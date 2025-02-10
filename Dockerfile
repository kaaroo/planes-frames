FROM python:3.11.3-slim-bullseye

WORKDIR /code

RUN apt-get update && apt-get -y install python3-pip
RUN python3 -m pip install poetry

RUN touch README.md
COPY .env /code/.env
COPY ./app /code/app
COPY pyproject.toml /code/pyproject.toml
COPY poetry.lock /code/poetry.lock
RUN poetry install --no-root --no-interaction --no-ansi

CMD ["poetry", "run", "python3", "-m", "uvicorn", "app.main:app", "--reload", "--env-file", ".env", "--host", "0.0.0.0", "--port", "8000"]