from sqlalchemy import create_engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app import models, schemas
from app.config import settings

from models import (
    Base,
    Truck,
    Route,
    Stop,
    Parcel,
    ThirdPartyPartner,
    Geofence,
    Alert,
)
load_dotenv()
DATABASE_URL = (
    f"postgresql://backventures_owner:{os.getenv('NEON_DB_PASSWORD')}@"
    f"ep-autumn-salad-a10uosov.ap-southeast-1.aws.neon.tech/backventures?sslmode=require"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# Create all tables
Base.metadata.create_all(engine)


def get_truck(truck_id):
    return session.query(Truck).filter(Truck.id == truck_id).first()


def update_truck(truck_id, truck):
    truck_obj = get_truck(truck_id)
    if truck_obj:
        truck_obj.capacity = truck.capacity
        truck_obj.current_load = truck.current_load
        truck_obj.route_id = truck.route_id
        truck_obj.location = truck.location
        truck_obj.status = truck.status
        session.commit()


def get_truck_location(truck_id):
    truck = get_truck(truck_id)
    if truck:
        return {"latitude": truck.latitude, "longitude": truck.longitude}
    return None


def update_truck_location(truck_id, location):
    truck = get_truck(truck_id)
    if truck:
        truck.latitude = location.get("latitude")
        truck.longitude = location.get("longitude")
        session.commit()
        return True
    return False

# Route operations


def get_route(route_id):
    return session.query(Route).filter(Route.id == route_id).first()


def update_route(route_id, route):
    route_obj = get_route(route_id)
    if route_obj:
        route_obj.name = route.name
        route_obj.distance = route.distance
        route_obj.stops = route.stops
        route_obj.trucks = route.trucks
        session.commit()


def get_stop(stop_id):
    return session.query(Stop).filter(Stop.id == stop_id).first()


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

# Reusable dependency to get the current authenticated user


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current authenticated user using the access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, credentials_exception)
    user = session.query(models.User).filter(
        models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user


def update_stop(stop_id, stop):
    stop_obj = get_stop(stop_id)
    if stop_obj:
        stop_obj.name = stop.name
        stop_obj.location = stop.location
        stop_obj.route_id = stop.route_id
        stop_obj.arrival_time = stop.arrival_time
        stop_obj.departure_time = stop.departure_time
        session.commit()


def get_all_stops_for_route(route_id):
    return session.query(Stop).filter(Stop.route_id == route_id).all()

# Parcel operations


def get_parcel(parcel_id):
    return session.query(Parcel).filter(Parcel.id == parcel_id).first()


def update_parcel(parcel_id, parcel):
    parcel_obj = get_parcel(parcel_id)
    if parcel_obj:
        parcel_obj.weight = parcel.weight
        parcel_obj.dimensions = parcel.dimensions
        parcel_obj.source = parcel.source
        parcel_obj.destination = parcel.destination
        parcel_obj.unload_at = parcel.unload_at
        session.commit()


def get_parcels_for_truck(truck_id):
    return session.query(Parcel).filter(Parcel.truck_id == truck_id).all()


def add_parcel(parcel):
    session.add(parcel)
    session.commit()


def remove_parcel(parcel_id):
    parcel = get_parcel(parcel_id)
    if parcel:
        session.delete(parcel)
        session.commit()

# Third-party partner operations


def get_third_party_partner(third_party_partner_id):
    return session.query(ThirdPartyPartner).filter(ThirdPartyPartner.id == third_party_partner_id).first()


def update_third_party_partner(third_party_partner_id, third_party_partner):
    third_party_partner_obj = get_third_party_partner(third_party_partner_id)
    if third_party_partner_obj:
        third_party_partner_obj.name = third_party_partner.name
        third_party_partner_obj.capacity = third_party_partner.capacity
        third_party_partner_obj.available_capacity = third_party_partner.available_capacity
        session.commit()


def get_available_capacity():
    partners = session.query(ThirdPartyPartner).all()
    return [{"id": partner.id, "available_capacity": partner.available_capacity} for partner in partners]

# Geofence operations


def get_geofences():
    return session.query(Geofence).all()


def get_alerts():
    return session.query(Alert).all()

# DVSOPL Logic for Dynamic Vehicle Space Optimization for Parcel Loading


def dvsopl(truck_id, parcels):
    """
    Optimizes parcel loading for a given truck based on its capacity.

    :param truck_id: ID of the truck to optimize for
    :param parcels: List of parcel objects to consider for loading
    :return: List of parcels that fit in the truck
    """
    truck = get_truck(truck_id)
    if not truck:
        raise ValueError("Truck not found")

    remaining_capacity = truck.capacity - truck.current_load
    selected_parcels = []

    # Sort parcels by highest priority
    parcels = sorted(parcels, key=lambda p: p.weight / p.volume, reverse=True)

    for parcel in parcels:
        if parcel.weight <= remaining_capacity:
            selected_parcels.append(parcel)
            remaining_capacity -= parcel.weight

    return selected_parcels


def load_parcels_to_truck(truck_id, parcel_ids):
    """
    Loads selected parcels onto the truck and updates the database.

    :param truck_id: ID of the truck
    :param parcel_ids: List of parcel IDs to load
    """
    truck = get_truck(truck_id)
    if not truck:
        raise ValueError("Truck not found")

    parcels = [get_parcel(parcel_id) for parcel_id in parcel_ids]
    selected_parcels = dvsopl(truck_id, parcels)

    # Load selected parcels
    for parcel in selected_parcels:
        parcel.truck_id = truck_id
        truck.current_load += parcel.weight

    session.commit()

# Utility functions for space utilization and capacity sharing


def get_truck_space_utilization(truck_id):
    truck = get_truck(truck_id)
    if truck:
        parcels = get_parcels_for_truck(truck_id)
        total_volume = sum([p.volume for p in parcels])
        total_weight = sum([p.weight for p in parcels])
        return {
            "truck_id": truck_id,
            "total_volume": total_volume,
            "total_weight": total_weight,
            "remaining_capacity": truck.capacity - total_volume,
        }
    return {"error": "Truck not found"}


def update_truck_space_utilization(truck_id, package_id, space_utilization):
    truck = get_truck(truck_id)
    parcel = get_parcel(package_id)
    if truck and parcel:
        truck.current_load += space_utilization
        session.commit()


def share_capacity(truck_id, third_party_partner_id, capacity):
    truck = get_truck(truck_id)
    partner = get_third_party_partner(third_party_partner_id)
    if truck and partner and capacity <= truck.capacity - truck.current_load:
        partner.available_capacity -= capacity
        truck.current_load += capacity
        session.commit()
