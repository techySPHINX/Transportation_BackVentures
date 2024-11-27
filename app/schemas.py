from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    id: str

class TruckBase(BaseModel):
    capacity: int = Field(...,
                          description="Total capacity of the truck in units")
    current_load: int = Field(...,
                              description="Current load of the truck in units")
    route_id: Optional[int] = Field(
        None, description="ID of the assigned route")
    latitude: Optional[float] = Field(
        None, description="Current latitude of the truck")
    longitude: Optional[float] = Field(
        None, description="Current longitude of the truck")
    status: str = Field(...,
                        description="Status of the truck (e.g., active, inactive, maintenance)")


class TruckCreate(TruckBase):
    pass


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
    name: str = Field(..., description="Name of the route")
    distance: float = Field(...,
                            description="Distance of the route in kilometers")
    start_point: str = Field(..., description="Starting point of the route")
    end_point: str = Field(..., description="Ending point of the route")
    intermediate_points: Optional[List[str]] = Field(
        None, description="List of intermediate points on the route"
    )


class RouteCreate(RouteBase):
    pass


class RouteResponse(RouteBase):
    id: int

    class Config:
        orm_mode = True

class StopBase(BaseModel):
    name: str = Field(..., description="Name of the stop")
    location: str = Field(..., description="Location of the stop")
    route_id: int = Field(..., description="ID of the associated route")
    arrival_time: datetime = Field(..., description="Arrival time at the stop")
    departure_time: datetime = Field(...,
                                     description="Departure time from the stop")


class StopCreate(StopBase):
    pass


class StopResponse(StopBase):
    id: int

    class Config:
        orm_mode = True


class ParcelBase(BaseModel):
    weight: float = Field(..., description="Weight of the parcel in kilograms")
    volume: float = Field(...,
                          description="Volume of the parcel in cubic meters")
    source: str = Field(..., description="Source location of the parcel")
    destination: str = Field(...,
                             description="Destination location of the parcel")
    truck_id: Optional[int] = Field(
        None, description="ID of the truck assigned to the parcel")


class ParcelCreate(ParcelBase):
    pass


class ParcelResponse(ParcelBase):
    id: int

    class Config:
        orm_mode = True


class PackageBase(BaseModel):
    weight: float = Field(...,
                          description="Weight of the package in kilograms")
    volume: float = Field(...,
                          description="Volume of the package in cubic meters")
    source: str = Field(..., description="Source location of the package")
    destination: str = Field(...,
                             description="Destination location of the package")
    truck_id: Optional[int] = Field(
        None, description="ID of the truck assigned to the package")


class PackageCreate(PackageBase):
    pass


class PackageResponse(PackageBase):
    id: int

    class Config:
        orm_mode = True


class ThirdPartyPartnerBase(BaseModel):
    name: str = Field(..., description="Name of the third-party partner")
    capacity: int = Field(...,
                          description="Total capacity provided by the partner")
    available_capacity: int = Field(...,
                                    description="Currently available capacity")


class ThirdPartyPartnerCreate(ThirdPartyPartnerBase):
    pass


class ThirdPartyPartnerResponse(ThirdPartyPartnerBase):
    id: int

    class Config:
        orm_mode = True


class GeofenceBase(BaseModel):
    route_id: int = Field(..., description="ID of the associated route")
    location: str = Field(...,
                          description="Central location of the geofence (latitude,longitude)")
    radius: float = Field(..., description="Radius of the geofence in meters")


class GeofenceCreate(GeofenceBase):
    pass


class GeofenceResponse(GeofenceBase):
    id: int

    class Config:
        orm_mode = True

class AlertBase(BaseModel):
    truck_id: int = Field(..., description="ID of the associated truck")
    geofence_id: int = Field(..., description="ID of the associated geofence")
    message: str = Field(..., description="Alert message")


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    timestamp: datetime = Field(...,
                                description="Timestamp when the alert was generated")

    class Config:
        orm_mode = True
