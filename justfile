set windows-shell := ["powershell", "-c"]

timestamp := if os_family() == "windows" {`[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()`} else {`date +%s`}

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

revision message:
    just exec api alembic revision --autogenerate -m "{{message}}"

upgrade id:
    just exec api alembic upgrade {{id}}

downgrade id:
    just exec api alembic downgrade {{id}}

backup:
    just exec db /scripts/backup.sh {{timestamp}}
    just exec redis /scripts/backup.sh {{timestamp}}

restore id:
    just exec db /scripts/restore.sh {{id}}
    just exec redis /scripts/restore.sh {{id}}
    just stop redis
    just start redis

test:
    just exec api pytest

lint:
    eslint ./frontend
    rye lint --pyproject ./api/pyproject.toml

format:
    prettier ./frontend
    rye format --pyproject ./api/pyproject.toml
