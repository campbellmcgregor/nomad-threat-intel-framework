"""NOMAD Web Intake GUI - FastAPI Application."""

from contextlib import asynccontextmanager
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

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

# Rate limiting middleware (simple in-memory)
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}
    
    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        # Clean up old requests
        self.requests = {ip: timestamps for ip, timestamps in self.requests.items() 
                         if timestamps and timestamps[-1] > now - 60}
        
        client_requests = self.requests.get(client_ip, [])
        # Filter requests from last minute
        client_requests = [t for t in client_requests if t > now - 60]
        
        if len(client_requests) >= self.requests_per_minute:
            return False
            
        client_requests.append(now)
        self.requests[client_ip] = client_requests
        return True

limiter = RateLimiter(requests_per_minute=60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting for static files and health checks
    if request.url.path.startswith("/static") or request.url.path.startswith("/health"):
        return await call_next(request)
        
    client_ip = request.client.host
    if not limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests"}
        )
    return await call_next(request)

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
