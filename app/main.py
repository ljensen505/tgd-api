from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routers.group.group import router as group_router
from app.routers.musicians.musicians import router as musicians_router
from app.routers.users.users import router as users_router
from app.routers.events.events import router as events_router
from app.routers.carousel.carousel import router as carousel_router
from dotenv import load_dotenv
import os
from app.auth.auth import VerifyToken

load_dotenv()


token_auth_scheme = HTTPBearer()

if os.getenv("env") == "prod":
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()


@app.get("/api/private")
async def private(token: HTTPAuthorizationCredentials = Depends(token_auth_scheme)):
    result = VerifyToken(token.credentials).verify()

    if result.get("status"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("msg")
        )

    return result


@app.get("/")
async def root():
    return {"msg": "The Grapefruits Duo API", "env": os.getenv("env")}


app.include_router(group_router, prefix="/group", tags=["group"])
app.include_router(musicians_router, prefix="/musicians", tags=["musicians"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(carousel_router, prefix="/carousel", tags=["carousel"])
