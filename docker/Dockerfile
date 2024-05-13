FROM python:3.12-alpine as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY ["pyproject.toml", "poetry.lock", "/app/"]

RUN pip install poetry && \
    poetry install --with prod

FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG GID=1000
ARG UID=1000
ARG USER=fastapi

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

RUN addgroup -g $GID -S $USER && \
    adduser -S $USER -G $USER --uid "$UID" && \
    chmod +x /app/docker/docker-entrypoint.sh

EXPOSE 8000

USER $USER

ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]

CMD ["gunicorn", "-c", "core/gunicorn.conf.py", "main:app"]
