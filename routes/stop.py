# routes/stops.py
from fastapi import APIRouter, HTTPException
from models import Stop
from db import get_stop, update_stop

router = APIRouter()

@router.get("/stops/")
async def read_stops():
    return get_stop()

@router.get("/stops/{stop_id}")
async def read_stop(stop_id: int):
    stop = get_stop(stop_id)
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")
    return stop

@router.put("/stops/{stop_id}")
async def update_stop(stop_id: int, stop: Stop):
    update_stop(stop_id, stop)
    return {"message": "Stop updated successfully"}