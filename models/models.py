from pydantic import BaseModel
from typing import Optional

class Truck(BaseModel):
    id: int
    capacity: int
    current_load: int
    route_id: int
    location: str
    status: str
    
class Route(BaseModel):
    id: int
    name: str
    distance: int
    start_point: str
    end_point: str
    intermediate_points: list[str]
    



class Stop(BaseModel):

    id: int
    name: str
    location: str
    route_id: int
    arrival_time: str
    departure_time: str

class Parcel(BaseModel):
    id: int
    weight: int
    volume: int
    source: str
    destination: str
    truck_id: int

class ThirdPartyPartner(BaseModel):
    id: int
    name: str
    capacity: int
    available_capacity: int
    
class Geofence(BaseModel):
    id: int
    route_id: int
    location: str
    radius: int
    
class Alert(BaseModel):
    id: int
    truck_id: int
    geofence_id: int
    message: str


