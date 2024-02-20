FROM python:3.12

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=0

WORKDIR /src

COPY ./pyproject.toml ./

RUN poetry install --no-root --no-interaction --no-cache

COPY ./src ./
