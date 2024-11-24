# routes/capacity_sharing.py
from fastapi import APIRouter, HTTPException
from models import Truck
from models import ThirdPartyPartner
from app.db import get_available_capacity, share_capacity, get_truck, get_third_party_partner

router = APIRouter()

@router.get("/capacity_sharing/available_capacity")
async def get_available_capacity():         
    return get_available_capacity()

@router.post("/capacity_sharing/share_capacity")
async def share_capacity(truck_id: int, third_party_partner_id: int, capacity: int):
    truck = get_truck(truck_id)
    third_party_partner = get_third_party_partner(third_party_partner_id)
    if not truck or not third_party_partner:
        raise HTTPException(status_code=404, detail="Truck or Third Party Partner not found")
    share_capacity(truck_id, third_party_partner_id, capacity)
    return {"message": "Capacity shared successfully"}
