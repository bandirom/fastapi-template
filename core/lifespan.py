from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: "FastAPI"):
    """
    Lifespan context manager for FastAPI application.
    Useful for initializing and cleaning up resources.
    """
    yield
