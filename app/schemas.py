from pydantic import BaseModel, Field
from typing import Optional, List

class TruckBase(BaseModel):
    capacity: int
    current_load: int
    route_id: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    status: str


class TruckCreate(TruckBase):
    pass  # Fields remain the same as TruckBase for creation.


class TruckUpdate(BaseModel):
    capacity: Optional[int]
    current_load: Optional[int]
    route_id: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    status: Optional[str]


class TruckResponse(TruckBase):
    id: int

    class Config:
        orm_mode = True

class RouteBase(BaseModel):
    name: str
    distance: int
    start_point: str
    end_point: str
    intermediate_points: List[str]


class RouteCreate(RouteBase):
    pass

class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True

class StopBase(BaseModel):
    name: str
    location: str
    route_id: int
    arrival_time: str
    departure_time: str


class StopCreate(StopBase):
    pass


class StopResponse(StopBase):
    id: int

    class Config:
        orm_mode = True

class ParcelBase(BaseModel):
    weight: int
    volume: int
    source: str
    destination: str
    truck_id: int


class ParcelCreate(ParcelBase):
    pass

class ParcelResponse(ParcelBase):
    id: int

    class Config:
        orm_mode = True

class ThirdPartyPartnerBase(BaseModel):
    name: str
    capacity: int
    available_capacity: int


class ThirdPartyPartnerCreate(ThirdPartyPartnerBase):
    pass


class ThirdPartyPartnerResponse(ThirdPartyPartnerBase):
    id: int

    class Config:
        orm_mode = True

class GeofenceBase(BaseModel):
    route_id: int
    location: str
    radius: int


class GeofenceCreate(GeofenceBase):
    pass

class GeofenceResponse(GeofenceBase):
    id: int

    class Config:
        orm_mode = True

class AlertBase(BaseModel):
    truck_id: int
    geofence_id: int
    message: str

class AlertCreate(AlertBase):
    pass

class AlertResponse(AlertBase):
    id: int

    class Config:
        orm_mode = True
