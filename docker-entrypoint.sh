#!/bin/bash
set -e

if [ ! -d "alembic" ]; then
    alembic init -t async alembic
    alembic revision --autogenerate -m "Create user"
    alembic upgrade head
fi

exec "$@"
