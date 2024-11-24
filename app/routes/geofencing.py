from fastapi import APIRouter, HTTPException
from app.utils import get_mapmyindia_access_token, get_vehicle_location, haversine
from app.db import get_truck_location, update_truck_location

router = APIRouter()

MAPMYINDIA_CLIENT_ID = "your_client_id"
MAPMYINDIA_CLIENT_SECRET = ""
access_token = get_mapmyindia_access_token(
    MAPMYINDIA_CLIENT_ID, MAPMYINDIA_CLIENT_SECRET)


@router.get("/geofence/track_vehicle")
async def track_vehicle(vehicle_id: str, start_lat: float, start_lon: float, geofence_radius_km: float):
    """
    Track a vehicle and check for geofence alerts.
    """
    try:
        curr_lat, curr_lon = get_vehicle_location(vehicle_id, access_token)
        distance = haversine(start_lat, start_lon, curr_lat, curr_lon)

        if distance >= geofence_radius_km:
            return {
                "alert": f"Vehicle {vehicle_id} has crossed the geofence radius of {geofence_radius_km} km.",
                "current_location": {"latitude": curr_lat, "longitude": curr_lon},
            }

        return {
            "message": f"Vehicle {vehicle_id} is within the geofence radius.",
            "current_location": {"latitude": curr_lat, "longitude": curr_lon},
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error tracking vehicle: {str(e)}")


@router.put("/geofence/update_truck_location")
async def update_truck_coordinates(truck_id: int, latitude: float, longitude: float):
    """
    Update truck's location in the database.
    """
    location = {"latitude": latitude, "longitude": longitude}
    success = update_truck_location(truck_id, location)

    if not success:
        raise HTTPException(
            status_code=404, detail="Truck not found or unable to update location.")

    return {"message": "Truck location updated successfully"}
