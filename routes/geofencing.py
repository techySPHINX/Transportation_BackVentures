# routes/geofencing.py
from fastapi import APIRouter, HTTPException
from models import Truck
from db import get_truck_location, update_truck_location, get_truck

router = APIRouter()

@router.get("/geofencing/truck_location")
async def get_truck_location(truck_id: int):
    truck = get_truck(truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return get_truck_location(truck_id)

@router.put("/geofencing/update_truck_location")
async def update_truck_location(truck_id: int, location: str):
    truck = get_truck(truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    update_truck_location(truck_id, location)
    return {"message": "Truck location updated successfully"}