from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import groups, lessons, health

app = FastAPI(title="myFlow API", version="0.0.1")

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
app.include_router(groups.router, prefix="/groups", tags=["groups"])
app.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
