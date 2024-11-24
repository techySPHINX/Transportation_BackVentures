import requests
import math


def get_mapmyindia_access_token(client_id, client_secret):
    """
    Fetch MapMyIndia access token.
    """
    url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials",
            "client_id": client_id, "client_secret": client_secret}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Unable to fetch MapMyIndia access token")


def get_vehicle_location(vehicle_id, access_token):
    """
    Fetch vehicle location using MapMyIndia API.
    """
    url = f"https://atlas.mapmyindia.com/api/advancedmaps/v1/track/{
        vehicle_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["latitude"], data["longitude"]
    else:
        raise Exception("Unable to fetch vehicle location")


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two coordinates using the Haversine formula.
    """
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
