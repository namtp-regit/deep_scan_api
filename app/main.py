from fastapi import FastAPI
from app.routes import items, users
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from app.database.connect import check_connection
from app.middleware.auth import AuthMiddleware

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

app = FastAPI(lifespan=lifespan)

# middleware authentication
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Base!"}