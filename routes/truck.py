# routes/trucks.py
from fastapi import APIRouter, HTTPException
from models import Truck
from db import get_truck, update_truck

router = APIRouter()

@router.get("/trucks/")
async def read_trucks():
    return get_truck()

@router.get("/trucks/{truck_id}")
async def read_truck(truck_id: int):
    truck = get_truck(truck_id)
    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")
    return truck

@router.put("/trucks/{truck_id}")
async def update_truck(truck_id: int, truck: Truck):
    update_truck(truck_id, truck)
    return {"message": "Truck updated successfully"}