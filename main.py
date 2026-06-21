"""
Bank App Backend - Main Entry Point
Vercel-compatible FastAPI application.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.api.v1.router import api_router
from app.middleware.cors_middleware import setup_cors
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.auth_middleware import AuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")
    yield
    print("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="US Bank App Backend with Crypto Integration",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Middleware
setup_cors(app)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

# Routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )
