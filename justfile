set windows-shell := ["powershell.exe", "-c"]

default:
    just --list

up:
    docker compose up -d

build:
    docker compose build

kill:
    docker compose kill

ps:
    docker compose ps

logs *args:
    docker-compose logs {{args}} -f

commit *args:
    docker compose exec api alembic revision --autogenerate -m "{{args}}"

upgrade:
    docker compose exec api alembic upgrade head

downgrade *args:
    docker compose exec api alembic downgrade {{args}}

lint:
    eslint ./frontend
    ruff check ./api/src

test:
    pytest ./api
