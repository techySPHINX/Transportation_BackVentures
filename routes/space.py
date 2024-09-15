# routes/space_utilization.py
from fastapi import APIRouter, HTTPException
from models import Truck
from models import Package
from db import get_truck_space_utilization, update_truck_space_utilization, get_truck, get_package

router = APIRouter()

@router.get("/space_utilization/truck_space_utilization")
async def get_truck_space_utilization(truck_id: int):
    truck = get_truck(truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return get_truck_space_utilization(truck_id)

@router.put("/space_utilization/update_truck_space_utilization")
async def update_truck_space_utilization(truck_id: int, package_id: int, space_utilization: int):
    truck = get_truck(truck_id)
    package = get_package(package_id)
    if not truck or not package:
        raise HTTPException(status_code=404, detail="Truck or Package not found")
    update_truck_space_utilization(truck_id, package_id, space_utilization)
    return {"message": "Truck space utilization updated successfully"}