#!/bin/bash
set -e

#if [ ! -d "alembic" ]; then
    alembic upgrade head
#fi

exec "$@"
