from fastapi import FastAPI
from app.routers.group.group import router as group_router
from app.routers.musicians.musicians import router as musicians_router
from app.routers.users.users import router as users_router
from app.routers.events.events import router as events_router
from dotenv import load_dotenv
from os import getenv

app = FastAPI()
load_dotenv()


@app.get("/")
async def root():
    return {"msg": "The Grapefruits Duo API", "env": getenv("env")}


app.include_router(group_router, prefix="/group", tags=["group"])
app.include_router(musicians_router, prefix="/musicians", tags=["musicians"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])
