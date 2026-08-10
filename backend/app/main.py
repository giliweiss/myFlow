import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import exercises, groups, lessons, health
from app.core.auth import is_dev_auth_bypass_enabled
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.dev_auth_bypass and settings.environment != "development":
        raise RuntimeError(
            "DEV_AUTH_BYPASS=true is only allowed when ENVIRONMENT=development"
        )

    if is_dev_auth_bypass_enabled():
        logger.warning(
            "*** DEV AUTH BYPASS IS ENABLED *** "
            "Protected endpoints accept requests without a valid Supabase JWT. "
            "Set DEV_AUTH_BYPASS=false before deploying."
        )

    yield


app = FastAPI(
    title="myFlow API",
    version="0.0.1",
    swagger_ui_parameters={"persistAuthorization": True},
    lifespan=lifespan,
)

# CORS - allow mobile apps to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["health"])
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
