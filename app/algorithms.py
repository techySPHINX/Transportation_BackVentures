from models import Parcel, Truck, Stop 
from typing import List, Dict
from sqlalchemy.orm import Session


def optimize_loading_space(api_key: str) -> Dict:
    """
    Optimizes the loading space of a truck by focusing on volume utilization,
    stackability, and orientation rules.
    """
    # Payload for the PTV Loading Space Optimization API
    payload = {
        "items": [
            {
                "id": "Large Packets",
                "numberOfInstances": 10,
                "dimensions": {"x": 120, "y": 80, "z": 180},
                "weight": 50000,
            },
            {
                "id": "Small Packets",
                "numberOfInstances": 5,
                "dimensions": {"x": 120, "y": 80, "z": 30},
                "weight": 70000,
            },
        ],
        "bins": [
            {
                "id": "Truck",
                "dimensions": {"x": 240, "y": 244, "z": 1360},
                "maximumWeightCapacity": 20000000,
            }
        ],
        "focus": "OPTIMIZE_VOLUME_UTILIZATION",
    }

    import requests

    url = "https://api.myptv.com/loading-space-optimization/v1/binPacking"
    headers = {"apiKey": api_key}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to optimize loading space", "details": response.text}


def dvso_pl(parcels: List[Parcel], truck: Truck, stops: List[str], db_session: Session) -> Dict:
    """
    Dynamic Volume Space Optimization with Priority Loading (DVSOPL)
    - Sorts parcels by volume and priority based on their unload points.
    - Manages intermediate stops for unloading and reloading.
    """
    # Step 1: Pre-process parcels
    # Descending volume, ascending unload point priority
    parcels.sort(key=lambda x: (-x.volume, x.unload_at))

    # Step 2: Loading the truck initially
    for parcel in parcels:
        layer = get_layer(parcel, truck)
        if truck.current_load + parcel.volume <= truck.capacity:
            truck.parcels.append((parcel, layer))
            truck.current_load += parcel.volume

    # Step 3: Process stops for unloading and reloading
    for stop in stops:
        # Unloading parcels at the stop
        truck.parcels = [
            (p, l) for p, l in truck.parcels if not should_unload(p, stop, truck)
        ]
        # Re-optimize after unloading
        truck.parcels.sort(key=lambda x: (-x[0].volume, x[0].unload_at))

        # Reloading parcels specific to this stop
        new_parcels = get_new_parcels_for_stop(
            stop, db_session) 
        for parcel in new_parcels:
            layer = get_layer(parcel, truck)
            if truck.current_load + parcel.volume <= truck.capacity:
                truck.parcels.append((parcel, layer))
                truck.current_load += parcel.volume

    report = generate_loading_report(truck)
    return report


def get_layer(parcel: Parcel, truck: Truck) -> int:
    """
    Determine the layer for a parcel based on its volume.
    """
    if parcel.volume > 0.5 * truck.capacity:
        return 1  # Lower layer for larger parcels
    elif parcel.volume < 0.2 * truck.capacity:
        return 3  # Upper layer for smaller parcels
    else:
        return 2  # Middle layer


def should_unload(parcel: Parcel, stop: str, truck: Truck) -> bool:
    """
    Determines if a parcel should be unloaded at a specific stop.
    """
    return parcel.unload_at == stop


def get_new_parcels_for_stop(stop: str, db_session: Session) -> List[Parcel]:
    """
    Retrieves new parcels for unloading at a given stop.
    """
    # Fetch parcels that need to be unloaded at this stop
    parcels_for_stop = db_session.query(
        Parcel).filter(Parcel.unload_at == stop).all()
    return parcels_for_stop


def generate_loading_report(truck: Truck) -> Dict:
    """
    Generates a detailed report of the truck's loading state.
    """
    report = {
        "truck_id": truck.id,
        "total_load": truck.current_load,
        "remaining_capacity": truck.capacity - truck.current_load,
        "loading_sequence": [
            {
                "parcel_id": p.id,
                "volume": p.volume,
                "weight": p.weight,
                "layer": l,
                "unload_at": p.unload_at,
            }
            for p, l in truck.parcels
        ],
    }
    return report
