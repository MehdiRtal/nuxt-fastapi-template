set windows-shell := ["powershell", "-c"]

default:
    just --list

up *args:
    docker compose --env-file ./.env --env-file ./api/prod.env up -d {{args}}

build *args:
    docker compose --env-file ./.env --env-file ./api/prod.env build {{args}}

commit *args:
    docker compose exec api alembic revision --autogenerate -m "{{args}}"

upgrade:
    docker compose exec api alembic upgrade head

downgrade *args:
    docker compose exec api alembic downgrade {{args}}

test:
    docker compose exec api pytest

lint:
    eslint ./frontend
    ruff check ./api/src

format:
    prettier ./frontend
    ruff format ./api/src
