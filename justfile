set windows-shell := ["powershell", "-c"]

default:
    just --list

up *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env up -d {{args}}

down *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env down {{args}}

build *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env build {{args}}

start *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env start {{args}}

stop *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env stop {{args}}

exec *args:
    docker compose --env-file ./.env --env-file ./api/.prod.env exec {{args}}

commit message:
    just exec api alembic revision --autogenerate -m "{{message}}"

upgrade id:
    just exec api alembic upgrade {{id}}

downgrade id:
    just exec api alembic downgrade {{id}}

backup:
    just exec db mkdir -p /backups
    just exec db pg_dump -Ft -U postgres -f /backups/dump.tar
    just exec redis redis-cli SAVE
    just exec redis mkdir -p /backups
    just exec redis cp /data/dump.rdb /backups/dump.rdb

restore:
    just exec db pg_restore /backups/dump.tar -Ft -U postgres -d postgres
    just exec redis cp /backups/dump.rdb /data/dump.rdb
    just stop redis
    just start redis

test:
    just exec api pytest

lint:
    eslint ./frontend
    ruff check ./api/src

format:
    prettier ./frontend
    ruff format ./api/src
