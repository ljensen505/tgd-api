from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from app.routers.group.group import router as group_router
from app.routers.musicians.musicians import router as musicians_router
from app.routers.users.users import router as users_router
from app.routers.events.events import router as events_router
from app.routers.carousel.carousel import router as carousel_router
from app.routers.headshots.headshots import router as headshots_router
from app.auth.auth import VerifyToken
from app.__version__ import __version__

from dotenv import load_dotenv
from os import getenv


load_dotenv()


token_auth_scheme = HTTPBearer()
app = FastAPI()

origins = ["http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(group_router, prefix="/group", tags=["group"])
app.include_router(musicians_router, prefix="/musicians", tags=["musicians"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(carousel_router, prefix="/carousel", tags=["carousel"])
app.include_router(headshots_router, prefix="/headshots", tags=["headshots"])


@app.get("/api/private")
async def private(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()  # type: ignore

    return result


@app.get("/")
async def root():
    return {
        "msg": "The Grapefruits Duo API",
        "env": getenv("ENV"),
        "version": f"v{__version__}",
    }
