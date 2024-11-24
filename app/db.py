from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from app.models import Truck, Route, Stop, Parcel, ThirdPartyPartner, Geofence, Alert


from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

engine = create_engine('postgresql://backventures_owner:os.env.NEON_DB_PASSWORD@ep-autumn-salad-a10uosov.ap-southeast-1.aws.neon.tech/backventures?sslmode=require')

Session = sessionmaker(bind=engine)

session = Session()


Base.metadata.create_all(engine)

from models import Truck, Route, Stop, Package, ThirdPartyPartner

def get_truck(truck_id):
    return session.query(Truck).filter(Truck.id == truck_id).first()

def update_truck(truck_id, truck):
    truck_obj = get_truck(truck_id)
    truck_obj.capacity = truck.capacity
    truck_obj.current_load = truck.current_load
    truck_obj.route_id = truck.route_id
    truck_obj.location = truck.location
    0
    truck_obj.status = truck.status
    session.commit()

def get_route(route_id):
    return session.query(Route).filter(Route.id == route_id).first()

def update_route(route_id, route):
    route_obj = get_route(route_id)
    route_obj.name = route.name
    route_obj.distance = route.distance
    route_obj.stops = route.stops
    route_obj.trucks = route.trucks
    session.commit()

def get_stop(stop_id):
    return session.query(Stop).filter(Stop.id == stop_id).first()

def update_stop(stop_id, stop):
    stop_obj = get_stop(stop_id)
    stop_obj.name = stop.name
    stop_obj.location = stop.location
    stop_obj.route_id = stop.route_id
    stop_obj.arrival_time = stop.arrival_time
    stop_obj.departure_time = stop.departure_time
    session.commit()

def get_package(package_id):
    return session.query(Package).filter(Package.id == package_id).first()

def update_package(package_id, package):
    package_obj = get_package(package_id)
    package_obj.weight = package.weight
    package_obj.dimensions = package.dimensions
    package_obj.source = package.source
    session.commit()
    

def get_third_party_partner(third_party_partner_id):
    return session.query(ThirdPartyPartner).filter(ThirdPartyPartner.id == third_party_partner_id).first()

def update_third_party_partner(third_party_partner_id, third_party_partner):
    third_party_partner_obj = get_third_party_partner(third_party_partner_id)
    third_party_partner_obj.name = third_party_partner.name
    third_party_partner_obj.capacity = third_party_partner.capacity
    third_party_partner_obj.available_capacity = third_party_partner.available_capacity
    session.commit()


def get_truck_location(truck_id):
    truck = get_truck(truck_id)
    if not truck:
        return None
    return {"latitude": truck.latitude, "longitude": truck.longitude}


def update_truck_location(truck_id, location):
    truck = get_truck(truck_id)
    if not truck:
        return False
    truck.latitude = location.get("latitude")
    truck.longitude = location.get("longitude")
    session.commit()
    return True
