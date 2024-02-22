set windows-shell := ["powershell", "-c"]

default:
    just --list

up *args:
    docker compose --env-file ./.env --env-file ./api/prod.env up -d {{args}}

build *args:
    docker compose --env-file ./.env --env-file ./api/prod.env build {{args}}

exec *args:
    docker compose --env-file ./.env --env-file ./api/prod.env exec {{args}}

commit *args:
    just exec api alembic revision --autogenerate -m "{{args}}"

upgrade:
    just exec api alembic upgrade head

downgrade *args:
    just exec api alembic downgrade {{args}}

test:
    just exec api pytest

lint:
    eslint ./frontend
    ruff check ./api/src

format:
    prettier ./frontend
    ruff format ./api/src
