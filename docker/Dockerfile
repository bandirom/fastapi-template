FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock alembic/ api/ core/ db/ alembic.ini main.py ./

RUN pip install poetry && \
    poetry install --with prod

#COPY . .

COPY ./docker/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

#EXPOSE 8000
#
#ENTRYPOINT ["./docker/docker-entrypoint.sh"]
#
#CMD ["gunicorn", "-c", "/core/gunicorn.conf.py", "main:app"]
