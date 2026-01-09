"""NOMAD Web Intake GUI - FastAPI Application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.config import get_settings
from app.database import init_db
from app.api import reports_router, sharing_router, health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown (nothing to do)


settings = get_settings()

app = FastAPI(
    title="NOMAD Web Intake GUI",
    description="Threat Intelligence Report Sharing Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(reports_router)
app.include_router(sharing_router)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to static landing page or API docs."""
    if settings.debug:
        return RedirectResponse(url="/api/docs")
    return RedirectResponse(url="/static/index.html")
