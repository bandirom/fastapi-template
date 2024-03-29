FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry install --with prod

COPY . .

EXPOSE 8000

COPY docker/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "-c", "core/gunicorn.conf.py", "main:app"]