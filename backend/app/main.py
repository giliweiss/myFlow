import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import exercises, group_lessons, groups, instructor_profile, lessons, health
from app.core.auth import is_dev_auth_bypass_enabled
from app.core.config import settings, validate_dev_auth_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_dev_auth_settings()

    if is_dev_auth_bypass_enabled():
        logger.warning(
            "*** DEV AUTH BYPASS IS ENABLED *** "
            "Protected endpoints use DEV_USER_ID=%s without a Supabase JWT. "
            "Set DEV_AUTH_BYPASS=false before deploying.",
            settings.dev_user_id,
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
app.include_router(
    instructor_profile.router,
    prefix="/instructor-profile",
    tags=["instructor-profile"],
)
app.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(group_lessons.router, prefix="/groups", tags=["lessons"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
