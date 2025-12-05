from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api import auth, users, gateway
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    # Startup: Create database tables
    await init_db()
    yield
    # Shutdown: cleanup if needed
    pass


app = FastAPI(
    title="LLMObs Core API",
    description="Core backend service for LLMObs platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(gateway.router, prefix="/api/gateway", tags=["gateway"])


@app.get("/")
async def root():
    return {"message": "LLMObs Core API", "version": "0.1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
