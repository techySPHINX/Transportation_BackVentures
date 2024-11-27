from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.utils import hash_password, verify_password
Base = declarative_base()


class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)
    current_load = Column(Integer, default=0)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(String, nullable=False)

    route = relationship("Route", back_populates="trucks")
    parcels = relationship("Parcel", back_populates="truck")
    alerts = relationship("Alert", back_populates="truck")
    packages = relationship("Package", back_populates="truck", lazy="joined")


class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    distance = Column(Float, nullable=True) 
    start_point = Column(String, nullable=False)
    end_point = Column(String, nullable=False)
    intermediate_points = Column(Text, nullable=True)

    trucks = relationship("Truck", back_populates="route")
    stops = relationship("Stop", back_populates="route")
    geofences = relationship("Geofence", back_populates="route")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True)

    def verify_password(self, password: str):
        return verify_password(password, self.password_hash)

class Stop(Base):
    __tablename__ = "stops"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"))
    arrival_time = Column(DateTime, nullable=True)
    departure_time = Column(DateTime, nullable=True)

    route = relationship("Route", back_populates="stops")


class Parcel(Base):
    __tablename__ = "parcels"
    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)  # Weight in kg
    volume = Column(Float, nullable=False)  # Volume in cubic meters
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=True)

    truck = relationship("Truck", back_populates="parcels")


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer, nullable=False) 
    # Volume of the package in cubic meters
    volume = Column(Integer, nullable=False)
    source = Column(String, nullable=False)  
    # Destination location of the package
    destination = Column(String, nullable=False)
    # Foreign key to Truck (if applicable)
    truck_id = Column(Integer, nullable=True)
    truck = relationship("Truck", back_populates="packages", lazy="joined")

class ThirdPartyPartner(Base):
    __tablename__ = "third_party_partners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)  # Total capacity in units
    available_capacity = Column(Integer, default=0)
    active = Column(Boolean, default=True)  # Status of the partner


class Geofence(Base):
    __tablename__ = "geofences"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    location = Column(String, nullable=False)
    radius = Column(Float, nullable=False) 

    route = relationship("Route", back_populates="geofences")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=False)
    geofence_id = Column(Integer, ForeignKey("geofences.id"), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    truck = relationship("Truck", back_populates="alerts")
    geofence = relationship("Geofence")
