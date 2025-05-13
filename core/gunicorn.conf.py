from multiprocessing import cpu_count

bind = ["0.0.0.0:8080"]
workers: int = cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
