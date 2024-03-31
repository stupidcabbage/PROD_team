from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LocationSchema(BaseModel):
    name: str
    longitude: float
    latitude: float


class BusinessType(Enum):
    organisation = "ООО"
    individual = "ИП"


class ParticipantSchema(BaseModel):
    name: str
    position: str
    phone_number: str


class AgentSchema(BaseModel):
    id: int
    name: str
    description: str
    phone_number: str  # regex
    photo: str  # link


class MeetingAddSchema(BaseModel):
    date: datetime  # DATEFORMAT: DD.MM.YYYY HH:MM:SS
    place: LocationSchema
    participants: list[ParticipantSchema]


class DocumentsSchema(BaseModel):
    id: int
    documents: list[str]


class MeetingSchema(MeetingAddSchema):
    id: int
    documents: DocumentsSchema | None = None
    agent: AgentSchema | None = None
    is_canceled: bool = False
    type: BusinessType
