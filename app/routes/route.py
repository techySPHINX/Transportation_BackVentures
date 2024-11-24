# routes/routes.py
from fastapi import APIRouter, HTTPException
from models import Route
from app.db import get_route, update_route

router = APIRouter()

@router.get("/routes/")
async def read_routes():
    return get_route()

@router.get("/routes/{route_id}")
async def read_route(route_id: int):
    route = get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.put("/routes/{route_id}")
async def update_route(route_id: int, route: Route):
    update_route(route_id, route)
    return {"message": "Route updated successfully"}
