# routes/dynamic_routing.py
from fastapi import APIRouter, HTTPException
from models import Route
from app.db import get_route, update_route

router = APIRouter()

@router.get("/dynamic_routing/route")
async def get_route(route_id: int):
    route = get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/dynamic_routing/update_route")
async def update_route(route_id: int, route: Route):
    route = get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    update_route(route_id, route)
    return {"message": "Route updated successfully"}
