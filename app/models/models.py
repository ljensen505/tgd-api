from datetime import datetime
from pydantic import BaseModel


class Headshot(BaseModel):
    id: str
    url: str
    musician_id: int


class Group(BaseModel):
    name: str
    bio: str


class CarouselImage(BaseModel):
    id: str
    url: str


class Musician(BaseModel):
    id: int
    name: str
    bio: str
    headshot_id: str


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
