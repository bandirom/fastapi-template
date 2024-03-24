FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN pip install poetry && \
    poetry install --with prod

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the uvicorn server
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]