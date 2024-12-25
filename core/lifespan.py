from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from database.connect import check_connection


# check app startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not check_connection():
            raise SQLAlchemyError("Database connection failed during startup")
        print("Database connected successfully!")
    except Exception as e:
        print(f"Error during lifespan startup: {e}")
        raise e

    yield
    print("Application is shutting down...")
