from pydantic import BaseModel
from typing import Optional

"""User GPS Request Body Structure"""


class UserGPS(BaseModel):
    resource_type: str
    id: str
    session_id: Optional[str] = None
    latitude: str
    longitude: str
    timestamp: str


class UsersSearchGPS(BaseModel):
    resource_type: str
    distance: str
    longitude: str
    latitude: str
    distance_unit: str


"""User Search Request Body Structure"""


class SaveTerm(BaseModel):
    phrase: str
    customer_id: str
    source_id: str
    timestamp: str


class SaveSearchTerm(BaseModel):
    term: str
    search_type: str


class GetSearchTerm(BaseModel):
    term: str
    search_type: str
    search_length: int


class GetGeneralTerm(BaseModel):
    term: str
    search_length: int
