from datetime import datetime
from pydantic import BaseModel


class Group(BaseModel):
    name: str
    bio: str


class Musician(BaseModel):
    id: int
    name: str
    bio: str
    headshot: str


class User(BaseModel):
    id: str
    name: str


class Event(BaseModel):
    id: int
    name: str
    date: datetime
    description: str
    image_url: str
    location: str
    ticket_url: str
