from multiprocessing import cpu_count
from os import environ

bind: list = ['0.0.0.0:8000']

workers: int = int(environ.get('GUNICORN_WORKERS', cpu_count() * 2 + 1))

threads: int = int(environ.get('GUNICORN_THREADS', 1))

worker_class: str = 'uvicorn.workers.UvicornWorker'

loglevel: str = 'info'

# Reload gunicorn worker if request count > max_requests
max_requests: int = 1000
max_requests_jitter: int = 200

timeout: int = int(environ.get('GUNICORN_TIMEOUT', 30))

keepalive: int = int(environ.get('GUNICORN_KEEP_ALIVE', 2))
