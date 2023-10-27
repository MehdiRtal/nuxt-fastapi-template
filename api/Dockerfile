FROM python:3.11-alpine

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app

COPY pyproject.toml ./

RUN poetry install --no-root --no-interaction --no-cache

COPY ./ ./

EXPOSE 8000
