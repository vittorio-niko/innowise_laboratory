"""
Main app module.
"""

from fastapi import FastAPI
import models
from database import engine
from api.routes import router

# Create DB tables
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title="Simple Book Collection API",
    description="API for book collection",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Connect router
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )