from typing import Optional
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    current_load = Column(Integer)
    route_id = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String)


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    distance = Column(Integer)
    start_point = Column(String)
    end_point = Column(String)
    intermediate_points = Column(String)


class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    route_id = Column(Integer)
    arrival_time = Column(String)
    departure_time = Column(String)


class Parcel(Base):
    __tablename__ = "parcels"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    volume = Column(Integer)
    source = Column(String)
    destination = Column(String)
    truck_id = Column(Integer)


class ThirdPartyPartner(Base):
    __tablename__ = "third_party_partners"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)  # Total capacity
    available_capacity = Column(Integer)


class Geofence(Base):
    __tablename__ = "geofences"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer)  # Foreign key to `Route`
    location = Column(String)  # Central location of the geofence
    radius = Column(Integer)  # Radius in meters


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    truck_id = Column(Integer)  # Foreign key to `Truck`
    geofence_id = Column(Integer)  # Foreign key to `Geofence`
    message = Column(String)
