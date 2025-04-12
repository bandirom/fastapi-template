ARG PYTHON_VERSION=3.13

FROM python:${PYTHON_VERSION}-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install poetry setuptools --upgrade

COPY pyproject.toml poetry.lock ./

RUN poetry install --with prod


FROM python:${PYTHON_VERSION}-alpine
ARG PYTHON_VERSION

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG GID=1000
ARG UID=1000
ARG USER=fastapi

RUN apk add --no-cache libffi && \
    addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID"

COPY --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages/ /usr/local/lib/python${PYTHON_VERSION}/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

RUN chmod +x /app/docker/docker-entrypoint.sh

EXPOSE 8000

USER $USER

ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]

CMD ["gunicorn", "-c", "core/gunicorn.conf.py", "main:app"]
